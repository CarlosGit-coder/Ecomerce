(() => {
  const dialog = document.querySelector('#orderDialog');
  if (!dialog) return;
  const form = document.querySelector('#orderForm');
  const feedback = dialog.querySelector('.form-feedback');
  let pickupFee = 0, address = {};
  const selectedParts = new Map(), existingParts = new Map();
  let cart = [];
  try { cart = JSON.parse(localStorage.getItem('bytecare_cart') || '[]'); } catch (_) { cart = []; }
  const money = n => new Intl.NumberFormat('pt-BR', {style:'currency', currency:'BRL'}).format(n || 0);
  const serviceSubtotal = () => cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const updateTotal = () => {
    const pickup = form.querySelector('[name=fulfillment]:checked')?.value === 'pickup';
    const added = [...selectedParts.values()].reduce((sum, part) => sum + Number(part.price), 0);
    document.querySelector('#partsTotal').textContent = money(added);
    document.querySelector('#orderTotal').textContent = money(serviceSubtotal() + added + (pickup ? pickupFee : 0));
    document.querySelector('#pickupCost').textContent = pickupFee ? `+ ${money(pickupFee)}` : 'Calcular';
  };
  const persistCart = () => {
    localStorage.setItem('bytecare_cart', JSON.stringify(cart));
    document.querySelector('#cartCount').textContent = cart.reduce((sum, item) => sum + item.quantity, 0);
    const root = document.querySelector('#cartItems'); root.replaceChildren();
    if (!cart.length) { const empty = document.createElement('p'); empty.className = 'cart-empty'; empty.textContent = 'Seu carrinho está vazio. Adicione serviços pelo catálogo.'; root.append(empty); }
    cart.forEach(item => {
      const row = document.createElement('div'); row.className = 'cart-row';
      const info = document.createElement('div'); info.className = 'cart-row-info';
      const title = document.createElement('strong'); title.textContent = item.name;
      const price = document.createElement('small'); price.textContent = `${money(item.price)} cada`; info.append(title, price);
      const controls = document.createElement('div'); controls.className = 'quantity-controls';
      const minus = document.createElement('button'); minus.type = 'button'; minus.textContent = '−'; minus.setAttribute('aria-label', `Diminuir ${item.name}`);
      const quantity = document.createElement('span'); quantity.textContent = item.quantity;
      const plus = document.createElement('button'); plus.type = 'button'; plus.textContent = '+'; plus.setAttribute('aria-label', `Aumentar ${item.name}`);
      const remove = document.createElement('button'); remove.type = 'button'; remove.className = 'cart-remove'; remove.textContent = 'Remover';
      minus.addEventListener('click', () => changeQuantity(item.id, -1)); plus.addEventListener('click', () => changeQuantity(item.id, 1)); remove.addEventListener('click', () => { cart = cart.filter(current => current.id !== item.id); persistCart(); });
      controls.append(minus, quantity, plus, remove);
      const subtotal = document.createElement('b'); subtotal.className = 'cart-row-total'; subtotal.textContent = money(item.price * item.quantity);
      row.append(info, controls, subtotal); root.append(row);
    });
    document.querySelector('#cartSubtotal').textContent = money(serviceSubtotal());
    document.querySelector('#continueCheckout').disabled = cart.length === 0;
    document.querySelector('#assemblyParts').hidden = !cart.some(item => item.assembly);
    updateTotal();
  };
  const changeQuantity = (id, amount) => {
    const item = cart.find(current => current.id === id); if (!item) return;
    item.quantity = Math.max(1, Math.min(20, item.quantity + amount)); persistCart();
  };
  const addToCart = button => {
    const id = button.dataset.id; const current = cart.find(item => item.id === id);
    if (current) current.quantity = Math.min(20, current.quantity + 1);
    else cart.push({id, name:button.dataset.name, price:Number(button.dataset.price), quantity:1, assembly:button.dataset.assembly === 'true'});
    persistCart();
    button.innerHTML = 'Adicionado <span>✓</span>'; setTimeout(() => { button.innerHTML = 'Adicionar ao carrinho <span>+</span>'; }, 1000);
  };
  const drawTags = (map, root, priced) => {
    root.replaceChildren();
    for (const part of map.values()) {
      const tag = document.createElement('div'); tag.className = 'selected-part';
      const label = document.createElement('span'); label.textContent = `${part.name}${priced ? ` · ${money(part.price)}` : ''}`;
      const remove = document.createElement('button'); remove.type = 'button'; remove.textContent = '×'; remove.setAttribute('aria-label', `Remover ${part.name}`);
      remove.addEventListener('click', () => { map.delete(part.id); drawTags(map, root, priced); updateTotal(); });
      tag.append(label, remove); root.append(tag);
    }
  };
  const bindPartSearch = (inputId, categoryId, suggestionsId, map, tagsId, priced) => {
    const input = document.querySelector(`#${inputId}`), category = document.querySelector(`#${categoryId}`);
    const results = document.querySelector(`#${suggestionsId}`), tags = document.querySelector(`#${tagsId}`);
    let timer;
    const search = async () => {
      const term = input.value.trim();
      if (term.length < 2 && !category.value) { results.replaceChildren(); results.classList.remove('open'); return; }
      try {
        const params = new URLSearchParams({q:term, categoria:category.value});
        const response = await fetch(`/api/pecas?${params}`), payload = await response.json();
        results.replaceChildren();
        for (const part of payload.items || []) {
          if (map.has(part.id)) continue;
          const option = document.createElement('button'); option.type = 'button'; option.className = 'part-suggestion';
          const details = document.createElement('span'), name = document.createElement('b'), kind = document.createElement('small');
          name.textContent = part.name; kind.textContent = part.category; details.append(name, kind);
          option.append(details);
          if (priced) { const price = document.createElement('strong'); price.textContent = money(part.price); option.append(price); }
          option.addEventListener('click', () => {
            if (priced && [...map.values()].some(current => current.category === part.category)) {
              feedback.textContent = `Já existe uma peça da categoria ${part.category}. Remova-a para escolher outra.`;
              feedback.classList.add('error'); return;
            }
            const counterpart = priced ? existingParts : selectedParts;
            const overlap = [...counterpart.values()].find(current => current.category === part.category);
            if (cart.some(item => item.assembly) && overlap) {
              feedback.textContent = priced
                ? `Você marcou que já tem uma peça de ${part.category}. Remova-a da lista de peças que já possui antes de incluir outra.`
                : `Você já incluiu uma peça de ${part.category} para montar. Remova-a antes de marcar outra.`;
              feedback.classList.add('error'); return;
            }
            map.set(part.id, part); drawTags(map, tags, priced); input.value = ''; results.replaceChildren(); results.classList.remove('open');
            feedback.textContent = ''; feedback.className = 'form-feedback'; updateTotal();
          });
          results.append(option);
        }
        if (!results.childElementCount) {
          if (!priced && term.length >= 2) {
            const custom = document.createElement('button'); custom.type = 'button'; custom.className = 'part-suggestion';
            const label = document.createElement('span'), name = document.createElement('b'), kind = document.createElement('small');
            name.textContent = `Adicionar “${term}”`; kind.textContent = category.value || 'Outra peça'; label.append(name, kind); custom.append(label);
            custom.addEventListener('click', () => {
              const id = `manual:${term.toLowerCase()}`;
              map.set(id, {id, name:term, category:category.value || 'Outra peça'});
              drawTags(map, tags, false); input.value = ''; results.replaceChildren(); results.classList.remove('open');
            });
            results.append(custom);
          } else {
            const empty = document.createElement('div'); empty.className = 'part-suggestion-empty'; empty.textContent = 'Nenhuma peça encontrada. Tente outro nome ou categoria.'; results.append(empty);
          }
        }
        results.classList.add('open');
      } catch (_) { results.replaceChildren(); }
    };
    input.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(search, 180); });
    category.addEventListener('change', search);
    document.addEventListener('click', event => { if (!event.target.closest(`#${inputId}`) && !event.target.closest(`#${suggestionsId}`) && !event.target.closest(`#${categoryId}`)) results.classList.remove('open'); });
  };
  bindPartSearch('assemblySearch', 'assemblyCategory', 'assemblySuggestions', selectedParts, 'selectedParts', true);
  bindPartSearch('existingSearch', 'existingCategory', 'existingSuggestions', existingParts, 'existingParts', false);
  document.querySelectorAll('.add-to-cart').forEach(button => button.addEventListener('click', () => addToCart(button)));
  const openCart = () => {
    feedback.textContent = ''; feedback.className = 'form-feedback';
    document.querySelector('#cartStep').hidden = false; document.querySelector('#checkoutStep').hidden = true;
    persistCart(); dialog.showModal();
  };
  document.querySelector('#openCart').addEventListener('click', openCart);
  document.querySelector('#continueCheckout').addEventListener('click', () => {
    if (!cart.length) return;
    document.querySelector('#cartStep').hidden = true; document.querySelector('#checkoutStep').hidden = false;
    form.querySelectorAll('input,textarea').forEach(el => { if (!['radio','checkbox'].includes(el.type)) el.value = ''; });
    form.querySelector('[name=fulfillment][value=dropoff]').checked = true;
    pickupFee = 0; address = {}; document.querySelector('#addressResult').textContent = '';
    selectedParts.clear(); existingParts.clear(); drawTags(selectedParts, document.querySelector('#selectedParts'), true); drawTags(existingParts, document.querySelector('#existingParts'), false); updateTotal();
  });
  document.querySelector('.back-to-cart').addEventListener('click', () => { document.querySelector('#checkoutStep').hidden = true; document.querySelector('#cartStep').hidden = false; });
  dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', e => { if (e.target === dialog) dialog.close(); });
  form.querySelectorAll('[name=fulfillment]').forEach(r => r.addEventListener('change', updateTotal));
  let cepTimer;
  document.querySelector('#cepInput').addEventListener('input', e => {
    const digits = e.target.value.replace(/\D/g,'').slice(0,8);
    e.target.value = digits.length > 5 ? `${digits.slice(0,5)}-${digits.slice(5)}` : digits;
    pickupFee = 0; address = {}; updateTotal();
    clearTimeout(cepTimer);
    if (digits.length === 8) cepTimer = setTimeout(async () => {
      const result = document.querySelector('#addressResult'); result.textContent = 'Consultando CEP…';
      try {
        const response = await fetch(`/api/cep/${digits}`), data = await response.json();
        if (!response.ok) throw new Error(data.error);
        address = data.address; pickupFee = data.pickup_fee;
        result.textContent = `✓ ${[address.logradouro,address.bairro,address.localidade,address.uf].filter(Boolean).join(', ') || 'CEP consultado'}`;
        updateTotal();
      } catch (error) { result.textContent = error.message || 'Não foi possível consultar este CEP.'; }
    }, 300);
  });
  form.addEventListener('submit', async e => {
    e.preventDefault(); feedback.textContent = ''; feedback.className = 'form-feedback';
    const button = form.querySelector('[type=submit]'); button.disabled = true; button.innerHTML = 'Enviando…';
    const data = Object.fromEntries(new FormData(form));
    data.items = cart.map(item => ({id:item.id, quantity:item.quantity}));
    data.parts = [...selectedParts.values()].map(part => ({id:part.id}));
    data.existing_parts = [...existingParts.values()].map(part => part.name);
    try {
      const response = await fetch('/api/pedidos', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)});
      const result = await response.json(); if (!response.ok) throw new Error(result.error || 'Não foi possível registrar seu pedido.');
      localStorage.removeItem('bytecare_cart');
      window.location.assign(result.whatsapp_url);
    } catch(error) { feedback.textContent = error.message; feedback.classList.add('error'); }
    finally { button.disabled = false; button.innerHTML = 'Comprar pelo WhatsApp <span>↗</span>'; }
  });
  persistCart();
  const requestedService = new URLSearchParams(window.location.search).get('adicionar');
  if (requestedService) {
    const requestedButton = [...document.querySelectorAll('.add-to-cart')].find(button => button.dataset.id === requestedService);
    if (requestedButton) { addToCart(requestedButton); openCart(); }
  }
  document.querySelector('.menu-toggle')?.addEventListener('click', e => {
    const open = document.querySelector('.site-header nav').classList.toggle('open');
    e.currentTarget.setAttribute('aria-expanded', open);
  });
})();
