document.addEventListener('DOMContentLoaded', function() {
    // Load sensitive items
    loadSensitiveItems();

    // Setup modals
    const addModal = document.getElementById('add-item-modal');
    const viewModal = document.getElementById('view-item-modal');
    const addBtn = document.getElementById('add-sensitive-item');
    const span = document.getElementsByClassName('close');

    addBtn.onclick = function() {
        setupItemFields();
        addModal.style.display = 'block';
    }

    for (let i = 0; i < span.length; i++) {
        span[i].onclick = function() {
            addModal.style.display = 'none';
            viewModal.style.display = 'none';
        }
    }

    window.onclick = function(event) {
        if (event.target == addModal) {
            addModal.style.display = 'none';
        }
        if (event.target == viewModal) {
            viewModal.style.display = 'none';
        }
    }

    // Lock vault button
    document.getElementById('lock-vault').addEventListener('click', function() {
        fetch('/unlock-vault', {
            method: 'DELETE'
        }).then(() => {
            window.location.href = '/unlock-vault';
        });
    });

    // Item type change handler
    document.getElementById('item-type').addEventListener('change', setupItemFields);
});

function setupItemFields() {
    const type = document.getElementById('item-type').value;
    const fieldsDiv = document.getElementById('item-fields');
    fieldsDiv.innerHTML = '';

    const fields = {
        'password': [
            {name: 'username', label: 'Username', type: 'text'},
            {name: 'password', label: 'Password', type: 'password'},
            {name: 'url', label: 'Website URL', type: 'url'},
            {name: 'notes', label: 'Notes', type: 'textarea'}
        ],
        'credit_card': [
            {name: 'card_number', label: 'Card Number', type: 'text'},
            {name: 'card_holder', label: 'Card Holder', type: 'text'},
            {name: 'expiry', label: 'Expiry Date', type: 'text'},
            {name: 'cvv', label: 'CVV', type: 'password'},
            {name: 'pin', label: 'PIN', type: 'password'},
            {name: 'notes', label: 'Notes', type: 'textarea'}
        ],
        'bank_account': [
            {name: 'account_number', label: 'Account Number', type: 'text'},
            {name: 'routing_number', label: 'Routing Number', type: 'text'},
            {name: 'bank_name', label: 'Bank Name', type: 'text'},
            {name: 'account_type', label: 'Account Type', type: 'text'},
            {name: 'notes', label: 'Notes', type: 'textarea'}
        ],
        'id': [
            {name: 'id_number', label: 'ID Number', type: 'text'},
            {name: 'full_name', label: 'Full Name', type: 'text'},
            {name: 'issue_date', label: 'Issue Date', type: 'date'},
            {name: 'expiry_date', label: 'Expiry Date', type: 'date'},
            {name: 'issuing_authority', label: 'Issuing Authority', type: 'text'},
            {name: 'notes', label: 'Notes', type: 'textarea'}
        ],
        'other': [
            {name: 'field1', label: 'Field 1', type: 'text'},
            {name: 'field2', label: 'Field 2', type: 'text'},
            {name: 'notes', label: 'Notes', type: 'textarea'}
        ]
    };

    fields[type].forEach(field => {
        const group = document.createElement('div');
        group.className = 'form-group';

        const label = document.createElement('label');
        label.htmlFor = field.name;
        label.textContent = field.label;

        let input;
        if (field.type === 'textarea') {
            input = document.createElement('textarea');
            input.className = 'form-control';
            input.id = field.name;
            input.rows = 3;
        } else {
            input = document.createElement('input');
            input.type = field.type;
            input.className = 'form-control';
            input.id = field.name;
        }

        group.appendChild(label);
        group.appendChild(input);
        fieldsDiv.appendChild(group);
    });

    // Setup save button
    document.getElementById('save-item').onclick = saveItem;
}

function saveItem() {
    const type = document.getElementById('item-type').value;
    const name = document.getElementById('item-name').value;
    const data = {};

    // Collect all field values
    document.querySelectorAll('#item-fields input, #item-fields textarea').forEach(field => {
        data[field.id] = field.value;
    });

    fetch('/api/sensitive', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            type: type,
            name: name,
            data: data
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            document.getElementById('add-item-modal').style.display = 'none';
            loadSensitiveItems();
        }
    });
}

function loadSensitiveItems() {
    fetch('/api/sensitive')
    .then(response => response.json())
    .then(items => {
        const container = document.getElementById('sensitive-items-list');
        container.innerHTML = '';

        if (items.length === 0) {
            container.innerHTML = '<p>No items in your vault yet. Click "Add New Item" to get started.</p>';
            return;
        }

        items.forEach(item => {
            const card = document.createElement('div');
            card.className = 'item-card';
            card.dataset.id = item.id;

            const icon = document.createElement('div');
            icon.className = 'item-icon';
            icon.innerHTML = getIconForType(item.type);

            const content = document.createElement('div');
            content.className = 'item-content';

            const title = document.createElement('h4');
            title.textContent = item.name;

            const type = document.createElement('span');
            type.className = 'item-type';
            type.textContent = item.type.replace('_', ' ');

            content.appendChild(title);
            content.appendChild(type);
            card.appendChild(icon);
            card.appendChild(content);

            card.addEventListener('click', () => viewItem(item));
            container.appendChild(card);
        });
    });
}

function viewItem(item) {
    const modal = document.getElementById('view-item-modal');
    const content = document.getElementById('item-details-content');
    const title = document.getElementById('view-item-title');

    title.textContent = item.name;
    content.innerHTML = '';

    const type = document.createElement('p');
    type.className = 'item-meta';
    type.innerHTML = `<strong>Type:</strong> ${item.type.replace('_', ' ')}`;
    content.appendChild(type);

    for (const [key, value] of Object.entries(item.data)) {
        if (!value) continue;

        const group = document.createElement('div');
        group.className = 'detail-group';

        const label = document.createElement('strong');
        label.textContent = `${key.replace('_', ' ')}: `;

        const val = document.createElement('span');
        val.textContent = value;

        if (key.toLowerCase().includes('password') || key.toLowerCase().includes('pin') || key.toLowerCase().includes('cvv')) {
            val.textContent = '••••••••';
            val.dataset.value = value;
            val.style.cursor = 'pointer';

            val.addEventListener('click', function() {
                if (this.textContent === '••••••••') {
                    this.textContent = this.dataset.value;
                } else {
                    this.textContent = '••••••••';
                }
            });
        }

        group.appendChild(label);
        group.appendChild(document.createElement('br'));
        group.appendChild(val);
        content.appendChild(group);
    }

    // Setup delete button
    document.getElementById('delete-item').onclick = function() {
        if (confirm('Are you sure you want to delete this item?')) {
            fetch(`/api/sensitive/${item.id}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    modal.style.display = 'none';
                    loadSensitiveItems();
                }
            });
        }
    };

    // Setup copy button
    document.getElementById('copy-item').onclick = function() {
        let textToCopy = `${item.name}\nType: ${item.type}\n\n`;
        
        for (const [key, value] of Object.entries(item.data)) {
            textToCopy += `${key.replace('_', ' ')}: ${value}\n`;
        }

        navigator.clipboard.writeText(textToCopy)
            .then(() => alert('Item details copied to clipboard'))
            .catch(err => console.error('Could not copy text: ', err));
    };

    modal.style.display = 'block';
}

function getIconForType(type) {
    const icons = {
        'password': '🔑',
        'credit_card': '💳',
        'bank_account': '🏦',
        'id': '🆔',
        'other': '📁'
    };
    return icons[type] || '📄';
}