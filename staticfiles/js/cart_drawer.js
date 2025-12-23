// Cart Drawer Functions
function openCartDrawer() {
  const drawer = document.getElementById('cart-drawer');
  const overlay = document.getElementById('cart-overlay');
  
  overlay.classList.remove('hidden');
  drawer.classList.remove('translate-x-full');
  document.body.style.overflow = 'hidden';
  
  loadCartItems();
}

function closeCartDrawer() {
  const drawer = document.getElementById('cart-drawer');
  const overlay = document.getElementById('cart-overlay');
  
  drawer.classList.add('translate-x-full');
  overlay.classList.add('hidden');
  document.body.style.overflow = '';
}

function loadCartItems() {
  fetch('/get_cart_items/')
    .then(response => response.json())
    .then(data => {
      const container = document.getElementById('cart-items-container');
      const emptyCart = document.getElementById('empty-cart');
      const totalElement = document.getElementById('cart-drawer-total');
      
      if (data.items && data.items.length > 0) {
        emptyCart.classList.add('hidden');
        container.innerHTML = data.items.map(item => `
          <div class="flex gap-4 pb-6 border-b border-gray-200 dark:border-gray-600 mb-4">
            <img src="${item.image}" alt="${item.name}" class="w-20 h-24 object-cover rounded-lg">
            <div class="flex-1">
              <h3 class="font-semibold text-gray-900 dark:text-text-main">${item.name}</h3>
              <p class="text-sm text-gray-600 dark:text-text-secondary">${item.size} / ${item.sleeve}</p>
              <p class="font-semibold text-primary mt-2">₹${item.price}</p>
              <div class="flex items-center justify-between mt-2">
                <span class="text-sm text-gray-600 dark:text-text-secondary">Qty: ${item.quantity}</span>
                <span class="font-semibold text-gray-900 dark:text-text-main">₹${item.total}</span>
              </div>
            </div>
          </div>
        `).join('');
        totalElement.textContent = `₹${data.cart_total}`;
      } else {
        emptyCart.classList.remove('hidden');
        container.innerHTML = '';
      }
    });
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
  const closeBtn = document.getElementById('close-cart-drawer');
  const overlay = document.getElementById('cart-overlay');
  
  if (closeBtn) {
    closeBtn.addEventListener('click', closeCartDrawer);
  }
  
  if (overlay) {
    overlay.addEventListener('click', closeCartDrawer);
  }
});
