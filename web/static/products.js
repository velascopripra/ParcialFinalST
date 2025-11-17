function getProducts() {
    fetch('/api/products')
        .then(response => response.json())
        .then(data => {
            console.log(data);

            const tableBody = document.querySelector('#product-list tbody');
            tableBody.innerHTML = '';

            data.forEach(product => {
                const row = document.createElement('tr');

                row.innerHTML = `
                    <td>${product.name}</td>
                    <td>${product.description}</td>
                    <td>${product.price}</td>
                    <td>${product.stock}</td>
                    <td>
                        <a href="/edit_product/${product.id}" class="btn btn-primary btn-sm mr-2">Edit</a>
                        <button class="btn btn-danger btn-sm" onclick="deleteProduct(${product.id})">Delete</button>
                    </td>
                `;

                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error:', error));
}

function createProduct() {
    const data = {
        name: document.getElementById('name').value,
        description: document.getElementById('description').value,
        price: parseFloat(document.getElementById('price').value),
        stock: parseInt(document.getElementById('stock').value)
    };

    fetch('/api/products', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        alert('Product created successfully');
        getProducts();
    })
    .catch(error => console.error('Error:', error));
}

function updateProduct() {
    const productId = document.getElementById('product-id').value;

    const data = {
        name: document.getElementById('name').value,
        description: document.getElementById('description').value,
        price: parseFloat(document.getElementById('price').value),
        stock: parseInt(document.getElementById('stock').value)
    };

    fetch(`/api/products/${productId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        alert('Product updated successfully');
        window.location.href = '/products';
    })
    .catch(error => console.error('Error:', error));
}

function deleteProduct(productId) {
    if (confirm('Are you sure you want to delete this product?')) {
        fetch(`/api/products/${productId}`, { method: 'DELETE' })
            .then(response => response.json())
            .then(data => {
                alert('Product deleted successfully');
                getProducts();
            })
            .catch(error => console.error('Error:', error));
    }
}

