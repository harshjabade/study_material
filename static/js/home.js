// ===========================
// STUDYHUB — HOME PAGE JS
// ===========================

// Hero search → redirect to materials page with query
function heroSearchRedirect() {
  const query = document.getElementById('heroSearch').value.trim();
  if (query) {
    window.location.href = `/materials/?search=${encodeURIComponent(query)}`;
  } else {
    window.location.href = '/materials/';
  }
}

// Allow pressing Enter in search box
document.addEventListener('DOMContentLoaded', function () {
  const input = document.getElementById('heroSearch');
  if (input) {
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') heroSearchRedirect();
    });
  }
});