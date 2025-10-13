document.addEventListener('DOMContentLoaded', () => {
  console.log("DOM fully loaded");

  const userId = document.getElementById('user-data').dataset.userId;
  console.log("User ID:", userId);

  const cards = document.querySelectorAll('.contact-card');
  console.log("Found contact cards:", cards.length);

  const container = document.querySelector('.chat-messages');
  const sendButton = document.querySelector('.chat-send-button');
  const messageInput = document.querySelector('.chat-input');


  sendButton.addEventListener('click', () => {
    const text = messageInput.value.trim();
    if (!text) return;

    const activeCard = document.querySelector('.contact-card.active');
    if (!activeCard) return;

    const contactId = activeCard.getAttribute('data-contact-id');

    fetch(`/messages/${contactId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text, senderId: userId })
    })
    .then(response => response.json())
    .then(data => {
      console.log("Message sent:", data);
      messageInput.value = '';
      activeCard.click();
    });
  });


  cards.forEach(card => {
    card.addEventListener('click', () => {
      document.querySelectorAll('.contact-card').forEach(c => c.classList.remove('active'));
      card.classList.add('active');

      const contactId = card.getAttribute('data-contact-id');
      console.log("Fetching messages for contact ID:", contactId);

      fetch(`/messages/${contactId}`)
        .then(response => response.json())
        .then(messages => {
          console.log("Messages received:", messages);
          container.innerHTML = '';

          messages.forEach(([text, senderId, date, time]) => {
            const div = document.createElement('div');
            div.className = 'message ' + (senderId == userId ? 'message-sent' : 'message-received');

            const content = document.createElement('div');
            content.className = 'message-text';
            content.textContent = text;

            const timestamp = document.createElement('div');
            timestamp.className = 'message-timestamp';
            const formattedTime = time.slice(0, 5);
            const [year, month, day] = date.split('-');
            const formattedDate = `${day}/${month}/${year.slice(2)}`;
            timestamp.textContent = `${formattedTime} — ${formattedDate}`;

            div.appendChild(content);
            div.appendChild(timestamp);
            container.appendChild(div);
          });
        });
    });
  });


  const popupButton = document.getElementById('add-contact-button');
  const popup = document.getElementById('add-contact-popup');
  popupButton.addEventListener('click', () => {
    popup.classList.toggle('hidden');
  });
});