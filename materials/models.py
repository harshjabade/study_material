from django.db import models

class User(models.Model):
    user_id    = models.AutoField(primary_key=True)
    name       = models.CharField(max_length=100)
    email      = models.CharField(max_length=100, unique=True)
    password   = models.CharField(max_length=255)
    course     = models.CharField(max_length=100)
    year       = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name


class Subject(models.Model):
    subject_id   = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=100)
    course       = models.CharField(max_length=100)
    semester     = models.CharField(max_length=20)

    class Meta:
        db_table = 'subjects'

    def __str__(self):
        return self.subject_name


class Material(models.Model):
    material_id = models.AutoField(primary_key=True)
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file_path   = models.CharField(max_length=255, blank=True, null=True)
    subject     = models.ForeignKey(
                    Subject,
                    on_delete=models.SET_NULL,
                    null=True,
                    db_column='subject_id'   # ← maps to your subject_id column
                  )
    uploaded_by = models.ForeignKey(
                    User,
                    on_delete=models.CASCADE,
                    null=True,
                    db_column='uploaded_by'  # ← maps to your uploaded_by column
                  )
    upload_date = models.DateTimeField(auto_now_add=True)
    downloads   = models.IntegerField(default=0)

    class Meta:
        db_table = 'materials'  # ← uses YOUR table, not materials_material

    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        return Like.objects.filter(material_id=self.material_id).count()

    @property
    def avg_rating(self):
        ratings = Rating.objects.filter(material_id=self.material_id)
        if ratings.exists():
            return round(sum(r.rating for r in ratings) / ratings.count(), 1)
        return 0.0


class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    material  = models.ForeignKey(Material, on_delete=models.CASCADE, db_column='material_id')
    user      = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    rating    = models.IntegerField()

    class Meta:
        db_table = 'ratings'
        unique_together = ('material', 'user')


class Comment(models.Model):
    comment_id   = models.AutoField(primary_key=True)
    material     = models.ForeignKey(Material, on_delete=models.CASCADE, db_column='material_id')
    user         = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comments'


class Like(models.Model):
    like_id  = models.AutoField(primary_key=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, db_column='material_id')
    user     = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')

    class Meta:
        db_table = 'likes'
        unique_together = ('material', 'user')