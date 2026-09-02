const clockElement = document.querySelector('#live-clock');

function updateClock() {
    const now = new Date();

    const options = {
        weekday: 'short',
        month: 'short',
        day: 'numeric'
    };

    const datePart = now.toLocaleDateString('en-US', options);

    const timePart = now.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });

    const full = `${datePart} ${timePart}`;

    clockElement.setAttribute('datetime', now.toISOString());
    clockElement.textContent = full;
}

updateClock();
setInterval(updateClock, 60000);
