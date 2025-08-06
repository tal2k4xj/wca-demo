// Shopping cart functionality
class ShoppingCart {
  constructor() {
    this.items = [];
    this.total = 0;
  }

  addItem(product, quantity = 1) {
    const existingItem = this.items.find(item => item.id === product.id);
    
    if (existingItem) {
      existingItem.quantity += quantity;
    } else {
      this.items.push({
        id: product.id,
        name: product.name,
        price: product.price,
        quantity
      });
    }
    
    this.calculateTotal();
  }

  removeItem(productId) {
    this.items = this.items.filter(item => item.id !== productId);
    this.calculateTotal();
  }

  calculateTotal() {
    this.total = this.items.reduce((sum, item) => {
      return sum + (item.price * item.quantity);
    }, 0);
  }

  applyDiscount(code) {
    // Call backend API to validate and apply discount
    fetch('/api/discount', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        total: this.total,
        code: code
      })
    })
    .then(response => response.json())
    .then(data => {
      this.total = data.discountedTotal;
    });
  }
} 