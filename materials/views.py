import os
import json
import functools
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import Material, Like, Rating, Subject, User, Comment


# ─────────────────────────────────────────────
# HELPER — Custom login check (uses session)
# ─────────────────────────────────────────────

def login_required_custom(view_func):
    """Custom login-required decorator that uses the session-based auth system."""
    @functools.wraps(view_func)  # Preserves original view name & metadata
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


# ─────────────────────────────────────────────
# HOME
# ─────────────────────────────────────────────
def home(request):
    # Latest 3 materials
    latest_materials = Material.objects.select_related('subject', 'uploaded_by') \
                                       .all() \
                                       .order_by('-upload_date')[:3]

    # Popular 3 materials — most downloaded
    popular_materials = Material.objects.select_related('subject', 'uploaded_by') \
                                        .all() \
                                        .order_by('-downloads')[:3]

    # # Attach avg_rating to popular materials
    # for m in popular_materials:
    #     m.avg_rating = m.avg_rating  # calls the property

    # Stats for hero section
    from django.db.models import Sum
    total_materials  = Material.objects.count()
    total_users      = User.objects.count()
    total_downloads  = Material.objects.aggregate(
                          total=Sum('downloads')
                       )['total'] or 0

    return render(request, 'home.html', {
        'latest_materials':  latest_materials,
        'popular_materials': popular_materials,
        'total_materials':   total_materials,
        'total_users':       total_users,
        'total_downloads':   total_downloads,
    })

def register_view(request):
    if request.method == 'POST':
        name            = request.POST.get('name', '').strip()
        email           = request.POST.get('email', '').strip()
        password        = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        course          = request.POST.get('course', '')
        year            = request.POST.get('year', '')
 
        # ── Validations ──
        if not all([name, email, password, course, year]):
            return render(request, 'register.html', {
                'error': 'All fields are required.'
            })
 
        if password != confirm_password:
            return render(request, 'register.html', {
                'error': 'Passwords do not match.'
            })
 
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {
                'error': 'This email is already registered. Please login.'
            })
 
        # ── Create user ──
        User.objects.create(
            name=name,
            email=email,
            password=password,   # NOTE: hash passwords in production!
            course=course,
            year=year
        )
 
        return redirect('login')
 
    return render(request, 'register.html')
 
 
# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────
 
def login_view(request):
    # If already logged in, go to materials
    if request.session.get('user_id'):
        return redirect('materials')
 
    if request.method == 'POST':
        email    = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
 
        if not email or not password:
            return render(request, 'login.html', {
                'error': 'Please enter both email and password.'
            })
 
        try:
            user = User.objects.get(email=email, password=password)
 
            # Save user info in session
            request.session['user_id']   = user.user_id
            request.session['user_name'] = user.name
            request.session['user_email'] = user.email
 
            return redirect('materials')
 
        except User.DoesNotExist:
            return render(request, 'login.html', {
                'error': 'Invalid email or password. Please try again.'
            })
 
    return render(request, 'login.html')
 
 
# ─────────────────────────────────────────────
# LOGOUT
# ─────────────────────────────────────────────
 
def logout_view(request):
    request.session.flush()   # clears all session data
    return redirect('login')
 
 

# ─────────────────────────────────────────────
# MATERIALS LIST
# ─────────────────────────────────────────────

@login_required_custom
def materials_view(request):
    # All materials with related subject and uploader
    materials = Material.objects.select_related('subject', 'uploaded_by').all().order_by('-upload_date')

    # Search query from the URL or search box
    search_query = request.GET.get('search', '').strip()
    if search_query:
        materials = materials.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(file_path__icontains=search_query) |
            Q(subject__subject_name__icontains=search_query) |
            Q(subject__course__icontains=search_query) |
            Q(uploaded_by__name__icontains=search_query) |
            Q(uploaded_by__course__icontains=search_query)
        )

    # All subjects for filter dropdown
    subjects = Subject.objects.all()

    # Current logged-in user
    user_id = request.session.get('user_id')

    # Materials this user has liked
    liked_ids = list(
        Like.objects.filter(user_id=user_id).values_list('material_id', flat=True)
    )

    # This user's ratings { material_id: rating_value }
    user_ratings = {
        r.material_id: r.rating
        for r in Rating.objects.filter(user_id=user_id)
    }

    # Pre-fetch comment counts for all materials in one query { material_id: count }
    from django.db.models import Count
    comment_counts = {
        row['material_id']: row['count']
        for row in Comment.objects.values('material_id').annotate(count=Count('comment_id'))
    }

    # Attach computed values to each material object
    for m in materials:
        m.user_rating    = user_ratings.get(m.material_id)
        m.likes          = m.likes_count
        m.rating         = m.avg_rating
        m.comment_count  = comment_counts.get(m.material_id, 0)  # default 0 if no comments

    return render(request, 'materials.html', {
        'materials': materials,
        'subjects':  subjects,
        'liked_ids': liked_ids,
        'search_query': search_query,
    })


# ─────────────────────────────────────────────
# UPLOAD
# ─────────────────────────────────────────────
@login_required_custom
def upload_view(request):
    subjects = Subject.objects.all()

    if request.method == 'POST':
        title      = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        subject_id = request.POST.get('subject_id')
        file       = request.FILES.get('file')
        user_id    = request.session.get('user_id')  # ← logged in user

        # Validate file
        if not file:
            return render(request, 'upload.html', {
                'error': 'Please select a file.',
                'subjects': subjects
            })

        allowed = ['pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'jpg', 'jpeg', 'png']
        ext = file.name.split('.')[-1].lower()
        if ext not in allowed:
            return render(request, 'upload.html', {
                'error': 'Unsupported file type! Allowed: PDF, DOC, PPT, XLS, JPG, PNG',
                'subjects': subjects
            })

        # Save file to media/materials/ folder
        import os
        from django.conf import settings
        file_path = os.path.join('materials', file.name)
        full_path = os.path.join(settings.MEDIA_ROOT, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, 'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        # Save to materials table with uploaded_by
        Material.objects.create(
            title          = title,
            description    = description,
            file_path      = file_path,
            subject_id     = subject_id if subject_id else None,
            uploaded_by_id = user_id,   # ← saves to uploaded_by column in DB
        )

        return redirect('materials')

    return render(request, 'upload.html', {'subjects': subjects})

# ─────────────────────────────────────────────
# DOWNLOAD
# ─────────────────────────────────────────────

@login_required_custom
def download_material(request, material_id):
    material = get_object_or_404(Material, material_id=material_id)

    # Increment download count
    material.downloads += 1
    material.save(update_fields=['downloads'])

    file_full_path = os.path.join(settings.MEDIA_ROOT, material.file_path)
    if not os.path.exists(file_full_path):
        raise Http404("File not found on server.")

    return FileResponse(
        open(file_full_path, 'rb'),
        as_attachment=True,
        filename=os.path.basename(material.file_path)
    )


# ─────────────────────────────────────────────
# LIKE (toggle)
# ─────────────────────────────────────────────

@login_required_custom
@require_POST
def like_material(request, material_id):
    material = get_object_or_404(Material, material_id=material_id)
    user_id  = request.session.get('user_id')

    existing = Like.objects.filter(material=material, user_id=user_id).first()

    if existing:
        existing.delete()
        liked = False
    else:
        Like.objects.create(material=material, user_id=user_id)
        liked = True

    return JsonResponse({
        'success': True,
        'liked':   liked,
        'likes':   material.likes_count,
    })


# ─────────────────────────────────────────────
# RATE
# ─────────────────────────────────────────────

@login_required_custom
@require_POST
def rate_material(request, material_id):
    material = get_object_or_404(Material, material_id=material_id)
    user_id  = request.session.get('user_id')

    try:
        data  = json.loads(request.body)
        value = int(data.get('rating', 0))
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'success': False, 'error': 'Invalid data'}, status=400)

    if value not in range(1, 6):
        return JsonResponse({'success': False, 'error': 'Rating must be 1 to 5'}, status=400)

    Rating.objects.update_or_create(
        material=material,
        user_id=user_id,
        defaults={'rating': value}
    )

    return JsonResponse({
        'success':    True,
        'avg_rating': material.avg_rating,
    })


# ─────────────────────────────────────────────
# COMMENTS
# ─────────────────────────────────────────────

@login_required_custom
@require_POST
def add_comment(request, material_id):
    material = get_object_or_404(Material, material_id=material_id)
    user_id  = request.session.get('user_id')

    try:
        data = json.loads(request.body)
        comment_text = data.get('comment_text', '').strip()
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'success': False, 'error': 'Invalid data'}, status=400)

    if not comment_text:
        return JsonResponse({'success': False, 'error': 'Comment cannot be empty'}, status=400)

    comment = Comment.objects.create(
        material=material,
        user_id=user_id,
        comment_text=comment_text
    )

    return JsonResponse({
        'success': True,
        'comment': {
            'id': comment.comment_id,
            'text': comment.comment_text,
            'date': comment.comment_date.strftime('%Y-%m-%d %H:%M'),
            'user_name': comment.user.name,
        }
    })


@login_required_custom
def get_comments(request, material_id):
    """Return all comments for a given material as JSON."""
    material = get_object_or_404(Material, material_id=material_id)

    comments = Comment.objects.filter(material=material).select_related('user').order_by('-comment_date')

    comments_data = [{
        'id': c.comment_id,
        'text': c.comment_text,
        'date': c.comment_date.strftime('%Y-%m-%d %H:%M'),
        'user_name': c.user.name,
    } for c in comments]

    return JsonResponse({'success': True, 'comments': comments_data})