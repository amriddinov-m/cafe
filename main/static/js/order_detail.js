let cart = [];
let currentCategory = 'all';

function initProducts(category = 'all') {
    const productsContainer = document.getElementById('products');
    const filteredProducts = category === 'all'
        ? products
        : products.filter(p => p.category === category);

    productsContainer.innerHTML = filteredProducts.map(product => `
                <div class="product-card bg-white rounded-lg shadow-md overflow-hidden transition-all duration-300">
                    <img src="${product.image}" alt="${product.name}" class="w-full h-48 object-cover">
                    <div class="p-4">
                        <h3 class="text-lg font-semibold">${product.name}</h3>
                        <p class="text-gray-600">$${product.price.toFixed(2)}</p>
                        <button onclick="addToCart(${product.id}, 1)"
                                class="mt-2 w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition-colors">
                            Выбрать
                        </button>
                    </div>
                </div>
            `).join('');
}

document.querySelectorAll('.category-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        currentCategory = e.target.dataset.category;
        initProducts(currentCategory);
    });
});

function addToCart(productId, quantity) {
    const product = products.find(p => p.id === productId);
    const existingItem = cart.find(item => item.id === productId);

    if (existingItem) {
        existingItem.quantity++;
    } else {
        cart.push({...product, quantity: quantity});
    }
    updateCart();
}

function updateCart() {
    const cartContainer = document.getElementById('cart-items');
    cartContainer.innerHTML = cart.map(item => `
                <div class="flex items-center justify-between bg-gray-50 p-4 rounded-lg">
                    <div>
                        <h4 class="font-semibold">${item.name}</h4>
                        <input type="hidden" name="product_${item.id}" value="${item.quantity}">
                        <p class="text-gray-600">$${item.price.toFixed(2)} x ${item.quantity}</p>
                    </div>
                    <div class="flex items-center space-x-2">
                        <button onclick="updateQuantity(${item.id}, ${item.quantity - 1})"
                                class="bg-gray-200 px-2 py-1 rounded">-</button>
                        <span>${item.quantity}</span>
                        <button onclick="updateQuantity(${item.id}, ${item.quantity + 1})"
                                class="bg-gray-200 px-2 py-1 rounded">+</button>
                    </div>
                </div>
            `).join('');

    updateTotals();
}

function updateQuantity(productId, newQuantity) {
    if (newQuantity < 1) {
        cart = cart.filter(item => item.id !== productId);
    } else {
        const item = cart.find(item => item.id === productId);
        item.quantity = newQuantity;
    }
    updateCart();
}

function updateTotals() {
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    document.getElementById('total').textContent = `$${total.toFixed(2)}`;
}

function clearCart() {
    cart = [];
    updateCart();
}

// Initialize the POS system
initProducts();

document.getElementById('search').addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    const filteredProducts = products.filter(product =>
        product.name.toLowerCase().includes(searchTerm) &&
        (currentCategory === 'all' || product.category === currentCategory)
    );

    const productsContainer = document.getElementById('products');
    productsContainer.innerHTML = filteredProducts.map(product => `
                <div class="product-card bg-white rounded-lg shadow-md overflow-hidden transition-all duration-300">
                    <img src="${product.image}" alt="${product.name}" class="w-full h-48 object-cover">
                    <div class="p-4">
                        <h3 class="text-lg font-semibold">${product.name}</h3>
                        <p class="text-gray-600">$${product.price.toFixed(2)}</p>
                        <button onclick="addToCart(${product.id}, 1)"
                                class="mt-2 w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition-colors">
                            Выбрать
                        </button>
                    </div>
                </div>
            `).join('');
});