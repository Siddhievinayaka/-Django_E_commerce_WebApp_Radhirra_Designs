function addToCart() {
  if (!isUserAuthenticated()) {
    showLoginModal();
    return;
  }
  
  // Disabled for now - may need in future
  // const selectedSize = document.querySelector('input[name="size"]:checked');
  // const selectedSleeve = document.querySelector('input[name="sleeve"]:checked');
  
  // Disabled validation - may need in future
  // if (!selectedSize) {
  //   alert('Please select a size');
  //   return;
  // }
  
  // if (!selectedSleeve) {
  //   alert('Please select a sleeve type');
  //   return;
  // }
  
  const csrftoken = getCookie('csrftoken');
  
  fetch('/add_to_cart/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({
      product_id: document.querySelector('[onclick="addToCart()"]').dataset.product,
      size: null, // selectedSize ? selectedSize.value : null,
      sleeve: null // selectedSleeve ? selectedSleeve.value : null
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      const cartTotal = document.getElementById('cart-total');
      if (cartTotal) {
        cartTotal.textContent = data.cart_items;
      }
      openCartDrawer();
    }
  });
}

function isUserAuthenticated() {
  return document.body.dataset.userAuthenticated === 'true';
}

function showLoginModal() {
  const modal = document.getElementById('login-modal');
  const overlay = document.getElementById('login-overlay');
  
  overlay.classList.remove('hidden');
  modal.classList.remove('translate-y-full');
  document.body.style.overflow = 'hidden';
}

function closeLoginModal() {
  const modal = document.getElementById('login-modal');
  const overlay = document.getElementById('login-overlay');
  
  modal.classList.add('translate-y-full');
  overlay.classList.add('hidden');
  document.body.style.overflow = '';
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function updateQuantity(itemId, action) {
  const csrftoken = getCookie('csrftoken');
  
  fetch('/update_cart_item/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({
      item_id: itemId,
      action: action
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      if (data.removed) {
        // Remove the entire cart item from DOM
        document.querySelector(`[data-item-id="${itemId}"]`).remove();
      } else {
        // Update quantity display
        document.querySelector(`[data-quantity="${itemId}"]`).textContent = data.quantity;
        // Update item total
        document.querySelector(`[data-item-total="${itemId}"]`).textContent = `₹${data.item_total}`;
      }
      
      // Update cart totals
      document.querySelector('[data-cart-total]').textContent = `₹${data.cart_total}`;
      
      // Update items count in summary
      const itemsCountElement = document.querySelector('.text-gray-600.dark\\:text-text-secondary');
      if (itemsCountElement) {
        itemsCountElement.innerHTML = `Items (${data.cart_items_count}) <span>₹${data.cart_total}</span>`;
      }
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

function removeItem(itemId) {
  const csrftoken = getCookie('csrftoken');
  
  fetch('/update_cart_item/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({
      item_id: itemId,
      action: 'remove'
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // Remove the entire cart item from DOM
      document.querySelector(`[data-item-id="${itemId}"]`).remove();
      
      // Update cart totals
      document.querySelector('[data-cart-total]').textContent = `₹${data.cart_total}`;
      
      // Update items count in summary
      const itemsCountElement = document.querySelector('.text-gray-600.dark\\:text-text-secondary');
      if (itemsCountElement) {
        itemsCountElement.innerHTML = `Items (${data.cart_items_count}) <span>₹${data.cart_total}</span>`;
      }
      
      // Check if cart is empty and reload page to show empty cart message
      if (data.cart_items_count === 0) {
        location.reload();
      }
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

// Size and sleeve selection
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.size-option').forEach(option => {
    option.addEventListener('click', function() {
      document.querySelectorAll('.size-option').forEach(opt => {
        opt.classList.remove('bg-primary', 'text-white', 'border-primary');
        opt.classList.add('bg-white', 'text-gray-900', 'border-gray-200');
      });
      this.classList.remove('bg-white', 'text-gray-900', 'border-gray-200');
      this.classList.add('bg-primary', 'text-white', 'border-primary');
      this.querySelector('input').checked = true;
    });
  });

  document.querySelectorAll('.sleeve-option').forEach(option => {
    option.addEventListener('click', function() {
      document.querySelectorAll('.sleeve-option').forEach(opt => {
        opt.classList.remove('bg-primary', 'text-white', 'border-primary');
        opt.classList.add('bg-white', 'text-gray-900', 'border-gray-200');
      });
      this.classList.remove('bg-white', 'text-gray-900', 'border-gray-200');
      this.classList.add('bg-primary', 'text-white', 'border-primary');
      this.querySelector('input').checked = true;
    });
  });
  
  // Login modal event listeners
  const closeLoginBtn = document.getElementById('close-login-modal');
  const loginOverlay = document.getElementById('login-overlay');
  
  if (closeLoginBtn) {
    closeLoginBtn.addEventListener('click', closeLoginModal);
  }
  
  if (loginOverlay) {
    loginOverlay.addEventListener('click', closeLoginModal);
  }
});