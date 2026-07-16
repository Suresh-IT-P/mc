// Configuration
const WHATSAPP_NUMBER = "+1234567890"; // To be updated by user

// Cart State
let cart = JSON.parse(localStorage.getItem('cart')) || [];

function saveCart() {
  localStorage.setItem('cart', JSON.stringify(cart));
  updateCartCount();
}

function addToCart(productId, quantity = 1) {
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
  let message = "Hello Moto MC Choice! I would like to place an order:\n\n";
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

// Initial setup on DOM Load
document.addEventListener('DOMContentLoaded', () => {
  updateCartCount();
  
  // Attach enter key to search
  const searchInput = document.getElementById('header-search');
  if (searchInput) {
    searchInput.addEventListener('keypress', function (e) {
      if (e.key === 'Enter') {
        executeSearch();
      }
    });
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

