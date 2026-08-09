// Configuration
const WHATSAPP_NUMBER = "+1234567890"; // To be updated by user

// Cart State
let cart = JSON.parse(localStorage.getItem('cart')) || [];

function saveCart() {
  localStorage.setItem('cart', JSON.stringify(cart));
  updateCartCount();
}
// Rate Limiter logic for buttons
let lastActionTime = 0;
const ACTION_THROTTLE_MS = 1000; // 1 second between clicks

function addToCart(productId, quantity = 1) {
  const now = Date.now();
  if (now - lastActionTime < ACTION_THROTTLE_MS) {
    console.warn("Rate limited: Please wait before adding to cart again.");
    return;
  }
  lastActionTime = now;

  const product = products.find(p => p.id === productId);
  if (!product) return;
  
  const existingItem = cart.find(item => item.id === productId);
  if (existingItem) {
    existingItem.quantity += quantity;
  } else {
    cart.push({ ...product, quantity });
  }
  
  saveCart();
  alert(`${product.name} added to cart!`);
}

function removeFromCart(productId) {
  cart = cart.filter(item => item.id !== productId);
  saveCart();
  if (typeof renderCart === 'function') renderCart();
}

function updateQuantity(productId, newQuantity) {
  if (newQuantity < 1) return removeFromCart(productId);
  const item = cart.find(i => i.id === productId);
  if (item) {
    item.quantity = newQuantity;
    saveCart();
    if (typeof renderCart === 'function') renderCart();
  }
}

function updateCartCount() {
  const countEl = document.getElementById('cart-count');
  if (countEl) {
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    countEl.innerText = totalItems;
  }
}

// WhatsApp Checkout
function checkoutViaWhatsApp(singleProduct = null, singleQuantity = 1) {
  const now = Date.now();
  if (now - lastActionTime < ACTION_THROTTLE_MS) {
    alert("Please wait a moment before sending another request.");
    return;
  }
  lastActionTime = now;

  let message = "Hello MotoChoice! I would like to place an order:\n\n";
  let total = 0;

  if (singleProduct) {
    // Direct buy from product page
    message += `- ${singleProduct.name} x${singleQuantity} (${formatPrice(singleProduct.price)})\n`;
    total = singleProduct.price * singleQuantity;
  } else {
    // Checkout from cart
    if (cart.length === 0) {
      alert("Your cart is empty!");
      return;
    }
    cart.forEach(item => {
      message += `- ${item.name} x${item.quantity} (${formatPrice(item.price * item.quantity)})\n`;
      total += item.price * item.quantity;
    });
  }

  message += `\n*Total Estimated:* ${formatPrice(total)}\n\n`;
  message += "Please let me know the payment details and shipping process.";

  const encodedMessage = encodeURIComponent(message);
  const whatsappUrl = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodedMessage}`;
  
  window.open(whatsappUrl, '_blank');
}

// Search functionality
function executeSearch() {
  const input = document.getElementById('header-search');
  if (input && input.value.trim() !== '') {
    window.location.href = `shop.html?search=${encodeURIComponent(input.value.trim())}`;
  }
}

function handleSearchInput(e) {
  const query = e.target.value.toLowerCase().trim();
  const suggestionsBox = document.getElementById('search-suggestions');
  
  if (!suggestionsBox) return;

  if (query.length < 2) {
    suggestionsBox.classList.remove('active');
    return;
  }

  const filtered = (typeof products !== 'undefined' ? products : []).filter(p => 
    p.name.toLowerCase().includes(query) || 
    p.category.toLowerCase().includes(query)
  ).slice(0, 5);

  if (filtered.length > 0) {
    suggestionsBox.innerHTML = filtered.map(p => `
      <div class="suggestion-item" onclick="window.location.href='product.html?id=${p.id}'">
        <img src="${p.image}" alt="${p.name}" class="suggestion-img">
        <div class="suggestion-info">
          <span class="suggestion-name">${p.name}</span>
          <span class="suggestion-price">${formatPrice(p.price)}</span>
        </div>
      </div>
    `).join('');
    suggestionsBox.classList.add('active');
  } else {
    suggestionsBox.innerHTML = '<div class="suggestion-item"><span class="suggestion-name">No results found</span></div>';
    suggestionsBox.classList.add('active');
  }
}

// Close suggestions on click outside
document.addEventListener('click', (e) => {
  const searchContainer = document.querySelector('.search-container');
  const suggestionsBox = document.getElementById('search-suggestions');
  if (searchContainer && suggestionsBox && !searchContainer.contains(e.target)) {
    suggestionsBox.classList.remove('active');
  }
});

// Initial setup on DOM Load
document.addEventListener('DOMContentLoaded', () => {
  updateCartCount();
  
  // Attach enter key and input event to search
  const searchInput = document.getElementById('header-search');
  
  // Basic debounce function to prevent rapid-fire search execution
  function debounce(func, timeout = 300){
    let timer;
    return (...args) => {
      clearTimeout(timer);
      timer = setTimeout(() => { func.apply(this, args); }, timeout);
    };
  }

  if (searchInput) {
    searchInput.addEventListener('keypress', function (e) {
      if (e.key === 'Enter') {
        executeSearch();
      }
    });
    searchInput.addEventListener('input', debounce(handleSearchInput, 300));
  }

  // Hero Carousel Logic
  const slides = document.querySelectorAll('.carousel-slide');
  const dots = document.querySelectorAll('.dot');
  if (slides.length > 0) {
    let currentSlide = 0;
    
    function showSlide(index) {
      slides.forEach(slide => slide.classList.remove('active'));
      dots.forEach(dot => dot.classList.remove('active'));
      
      slides[index].classList.add('active');
      dots[index].classList.add('active');
    }
    
    window.nextSlide = function() {
      currentSlide = (currentSlide + 1) % slides.length;
      showSlide(currentSlide);
    }
    
    window.prevSlide = function() {
      currentSlide = (currentSlide - 1 + slides.length) % slides.length;
      showSlide(currentSlide);
    }
    
    window.goToSlide = function(index) {
      currentSlide = index;
      showSlide(currentSlide);
    }
    
    // Auto slide
    setInterval(nextSlide, 5000);
  }
});

// Horizontal Scrolling
function scrollRow(id, direction) {
  const container = document.getElementById(id);
  if (container) {
    const scrollAmount = 300;
    if (direction === 'left') {
      container.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    } else {
      container.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    }
}
}

// Security Features
document.addEventListener('DOMContentLoaded', () => {
  // Disable right-click
  document.addEventListener('contextmenu', e => e.preventDefault());

  // Disable common developer tools keyboard shortcuts
  document.addEventListener('keydown', e => {
    // F12, Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+Shift+C, Ctrl+U
    if (
      e.key === 'F12' || 
      (e.ctrlKey && e.shiftKey && ['I', 'i', 'J', 'j', 'C', 'c'].includes(e.key)) ||
      (e.ctrlKey && ['U', 'u'].includes(e.key))
    ) {
      e.preventDefault();
    }
  });

  // Disable dragging images
  document.addEventListener('dragstart', e => {
    if (e.target.tagName === 'IMG') {
      e.preventDefault();
    }
  });
});
