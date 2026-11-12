(() => {
  const dialog = document.querySelector('#serviceDialog'); if (!dialog) return;
  const form = document.querySelector('#serviceEditForm');
  const fields = ['id','name','category','price','duration','icon','description','imageUrl'];
  const fill = data => {
    fields.forEach(key => { const el = document.querySelector(`#edit${key[0].toUpperCase()}${key.slice(1)}`); if (el) el.value = data[key] || ''; });
    document.querySelector('#editFeatured').checked = data.featured === 'true';
    document.querySelector('#editAssembly').checked = data.assembly === 'true';
    document.querySelector('#editActive').checked = data.active !== 'false';
    document.querySelector('#serviceFormTitle').innerHTML = data.id ? 'Editar <em>item.</em>' : 'Novo <em>item.</em>';
    dialog.showModal();
  };
  document.querySelector('#newService')?.addEventListener('click', () => { form.reset(); fill({}); });
  document.querySelectorAll('.edit-service').forEach(button => button.addEventListener('click', () => fill(button.dataset)));
  dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', e => { if (e.target === dialog) dialog.close(); });
})();
