function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let c = decodedCookie.split(';');

    for (let i = 0; i < c.length; i++) {
        let ca = c[i];
        while (ca.charAt(0) == ' ') {
            ca = ca.substring(1);
        }
        if (ca.indexOf(name) == 0) {
            return ca.substring(name.length, ca.length);
        }
    }
    return "";
}


function checkAuthentication(token) {
    const loginLink = document.getElementById('login-link');
    if (!token) {
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', async function () {
    const token = getCookie('token');
    checkAuthentication(token);
    try {
        const response = await fetch("http://127.0.0.1:6010/api/v1/places", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        });

        if (response.ok) {
            const data = await response.json();
            displayPlaces(data);
        } else {
            console.error(`Response error: ${response.status} - ${response.statusText}`);
        }
    } catch (error) {
        console.error(`Fetch error: ${error}`);
    }
});

function displayPlaces(places) {
    const placeList = document.querySelector('#places-list');
    const priceFilter = document.querySelector('#price-filter');
    placeList.textContent = '';


    places.forEach(({ title, price, id }) => {
        const placeCard = document.createElement('div');
        placeCard.className = "place-card";

        const placeContent = document.createElement('div');
        placeContent.className = "place-content";

        placeContent.innerHTML = `
            <div class="place-header">${title}</div>
            <div class="place-price">Price per night: ${price}</div>
        `;

        const placeButton = document.createElement('button');
        placeButton.className = "place-button";
        placeButton.onclick = () => {
            window.location = `http://127.0.0.1:5500/place.html?place_id=${id}`;
        };
        placeButton.textContent = 'View Details';

        placeContent.appendChild(placeButton);
        placeCard.appendChild(placeContent);
        placeList.appendChild(placeCard);
    });

    priceFilter.addEventListener('change', (event) => {
        const value = Number(event.target.value);
        const nodeList = document.querySelectorAll('.place-content');
        nodeList.forEach(node => {
            const price = Number(node.children[1].textContent.split(': ')[1]);
            node.parentElement.style.display = value && price > value ? 'none' : 'block';
        });
    });
}