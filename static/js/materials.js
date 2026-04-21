// ===========================
// STUDYHUB — MATERIALS JS
// ===========================

// ── FILTER & SEARCH ──────────────────────────────
function applyFilters() {
  const course   = document.getElementById("course").value.toLowerCase();
  const semester = document.getElementById("semester").value;
  const subject  = document.getElementById("subject").value.toLowerCase();
  const search   = document.getElementById("searchInput").value.toLowerCase().trim();

  const cards = document.querySelectorAll(".material-card");
  let visible = 0;

  cards.forEach(card => {
    const title    = card.dataset.title || "";
    const c        = card.dataset.course || "";
    const s        = card.dataset.semester || "";
    const sub      = card.dataset.subject || "";
    const desc     = card.dataset.description || "";
    const uploader = card.dataset.uploader || "";
    const filepath = card.dataset.filepath || "";

    let show = true;

    if (search && !title.includes(search) && !sub.includes(search) && !c.includes(search) && !desc.includes(search) && !uploader.includes(search) && !filepath.includes(search))
      show = false;
    if (course   && course   !== c)   show = false;
    if (semester && semester !== s)   show = false;
    if (subject  && subject  !== sub) show = false;

    card.style.display = show ? "block" : "none";
    if (show) visible++;
  });

  // Update count
  const el = document.getElementById("results-count");
  if (el) el.textContent = `${visible} material(s) found`;
}

function resetFilters() {
  document.getElementById("course").value       = "";
  document.getElementById("semester").value     = "";
  document.getElementById("subject").value      = "";
  document.getElementById("searchInput").value  = "";
  applyFilters();
}

function getQueryParam(name) {
  const params = new URLSearchParams(window.location.search);
  return params.get(name) || '';
}

// Auto-apply filters when the page loads
document.addEventListener('DOMContentLoaded', function () {
  const existingSearch = getQueryParam('search');
  if (existingSearch) {
    const input = document.getElementById('searchInput');
    if (input) {
      input.value = existingSearch;
    }
  }
  applyFilters();
});

// ── CSRF helper ──────────────────────────────────
function getCookie(name) {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  return match ? decodeURIComponent(match[2]) : null;
}

// ── TOAST ─────────────────────────────────────────
function showToast(msg, isError = false) {
  const t = document.getElementById("toast");
  if (!t) return;
  t.textContent = msg;
  t.style.borderLeftColor = isError ? "#ff6584" : "#6c63ff";
  t.classList.remove("hidden");
  setTimeout(() => t.classList.add("hidden"), 2800);
}

// ── LIKE ──────────────────────────────────────────
function likeMaterial(materialId, btn) {
  fetch(`/like/${materialId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "Content-Type": "application/json",
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      const counter = document.getElementById(`like-count-${materialId}`);
      if (counter) counter.textContent = data.likes;
      btn.classList.toggle("liked", data.liked);
      showToast(data.liked ? "👍 Liked!" : "Like removed");
    } else {
      showToast(data.error || "Something went wrong", true);
    }
  })
  .catch(() => showToast("Network error. Please try again.", true));
}

// ── RATE ──────────────────────────────────────────
function rateMaterial(materialId, value, selectEl) {
  if (!value) return;

  fetch(`/rate/${materialId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ rating: value })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      const ratingEl = document.getElementById(`rating-${materialId}`);
      if (ratingEl) ratingEl.textContent = parseFloat(data.avg_rating).toFixed(1);
      showToast(`⭐ Rated ${value} star${value > 1 ? "s" : ""}!`);
    } else {
      showToast(data.error || "Rating failed", true);
      if (selectEl) selectEl.value = "";
    }
  })
  .catch(() => showToast("Network error. Please try again.", true));
}

// ── COMMENTS ───────────────────────────────────────
let currentCommentMaterialId = null;

/**
 * Opens the comment modal for a given material.
 * @param {string} materialId - The ID of the material
 * @param {string} materialTitle - The title to display in the modal header
 */
function openComments(materialId, materialTitle) {
  var modal    = document.getElementById("commentModal");
  var input    = document.getElementById("commentInput");
  var list     = document.getElementById("commentsList");
  var subtitle = document.getElementById("modalMaterialTitle");

  // Guard: all modal elements must be present
  if (!modal || !input || !list) {
    console.error("Comment modal elements not found in DOM.");
    return;
  }

  // Track which material the modal is open for (used by submitComment)
  currentCommentMaterialId = materialId;

  // Update modal subtitle with material title
  if (subtitle && materialTitle) {
    subtitle.textContent = materialTitle;
  }

  // Show loading state and open modal
  list.innerHTML = '<div class="loading">Loading comments...</div>';
  modal.style.display = "flex";

  // Fetch existing comments from the server
  fetch("/comments/" + materialId + "/", {
    method: "GET",
    headers: { "X-CSRFToken": getCookie("csrftoken") }
  })
  .then(function(res) { return res.json(); })
  .then(function(data) {
    if (data.success) {
      renderComments(data.comments);
    } else {
      list.innerHTML = '<div class="error-msg">Failed to load comments.</div>';
    }
  })
  .catch(function() {
    list.innerHTML = '<div class="error-msg">Network error. Please try again.</div>';
  });
}

function renderComments(comments) {
  var list = document.getElementById("commentsList");
  if (!list) return;

  if (!comments || comments.length === 0) {
    list.innerHTML = '<div class="no-comments">No comments yet. Be the first to comment!</div>';
    return;
  }

  var html = "";
  for (var i = 0; i < comments.length; i++) {
    var c = comments[i];
    html += '<div class="comment-item">' +
      '<div class="comment-header">' +
        '<span class="comment-user">' + escapeHtml(c.user_name) + '</span>' +
        '<span class="comment-date">' + c.date + '</span>' +
      '</div>' +
      '<div class="comment-text">' + escapeHtml(c.text) + '</div>' +
    '</div>';
  }
  list.innerHTML = html;
}

/**
 * Posts a new comment and updates the UI immediately.
 */
function submitComment() {
  if (!currentCommentMaterialId) return;

  var input       = document.getElementById("commentInput");
  var commentText = input.value.trim();

  if (!commentText) {
    showToast("Please write a comment first", true);
    return;
  }

  fetch("/comment/add/" + currentCommentMaterialId + "/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ comment_text: commentText })
  })
  .then(function(res) { return res.json(); })
  .then(function(data) {
    if (data.success) {
      showToast("✅ Comment posted!");
      input.value = "";

      // Remove "No comments" placeholder if present
      var commentsList = document.getElementById("commentsList");
      var noComments   = commentsList.querySelector(".no-comments");
      if (noComments) noComments.remove();

      // Prepend the new comment to the list
      var newCommentHtml =
        '<div class="comment-item">' +
          '<div class="comment-header">' +
            '<span class="comment-user">' + escapeHtml(data.comment.user_name) + '</span>' +
            '<span class="comment-date">' + data.comment.date + '</span>' +
          '</div>' +
          '<div class="comment-text">' + escapeHtml(data.comment.text) + '</div>' +
        '</div>';
      commentsList.insertAdjacentHTML("afterbegin", newCommentHtml);

      // Update the comment count badge on the card button
      var countEl = document.getElementById("comment-count-" + currentCommentMaterialId);
      if (countEl) {
        var newCount = parseInt(countEl.textContent, 10) + 1;
        countEl.textContent = newCount;
        // Update the "Comment" / "Comments" label in the button text node
        var btn = document.getElementById("comment-btn-" + currentCommentMaterialId);
        if (btn) {
          // The button text node follows the span
          btn.childNodes.forEach(function(node) {
            if (node.nodeType === Node.TEXT_NODE) {
              node.textContent = " Comment" + (newCount !== 1 ? "s" : "");
            }
          });
        }
      }
    } else {
      showToast(data.error || "Failed to post comment", true);
    }
  })
  .catch(function() { showToast("Network error. Please try again.", true); });
}

function closeComments() {
  const modal = document.getElementById("commentModal");
  if (modal) modal.style.display = "none";
  currentCommentMaterialId = null;
}

// Close modal on outside click (but NOT when clicking the open button itself)
document.addEventListener("click", function(e) {
  const modal = document.getElementById("commentModal");
  if (modal && modal.style.display !== "none") {
    // Ignore clicks on the comment button that opened the modal
    if (e.target.closest(".btn-comment")) return;
    // Close only if click landed on the backdrop (outside .modal-content)
    if (e.target === modal || e.target.closest(".modal-content") === null) {
      closeComments();
    }
  }
});

// Allow Enter to submit comment
document.getElementById("commentInput")?.addEventListener("keypress", function(e) {
  if (e.key === "Enter") submitComment();
});

// Helper to escape HTML
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}