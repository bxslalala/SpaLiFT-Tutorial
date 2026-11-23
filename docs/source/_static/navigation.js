/* Keyboard semantics for the theme's icon-based mobile menu. */
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('[data-toggle="wy-nav-top"]');
  const sidebar = document.querySelector('.wy-nav-side');
  if (!toggle || !sidebar) return;
  sidebar.id = 'documentation-navigation';
  toggle.setAttribute('role', 'button');
  toggle.setAttribute('tabindex', '0');
  toggle.setAttribute('aria-label', 'Toggle navigation');
  toggle.setAttribute('aria-controls', sidebar.id);
  const sync = () => toggle.setAttribute('aria-expanded', String(sidebar.classList.contains('shift')));
  sync();
  new MutationObserver(sync).observe(sidebar, { attributes: true, attributeFilter: ['class'] });
  toggle.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      toggle.click();
    }
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && sidebar.classList.contains('shift')) {
      toggle.click();
      toggle.focus();
    }
  });
});
