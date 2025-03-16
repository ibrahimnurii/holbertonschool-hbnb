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

function getPlaceIdFromURL() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const placeId = urlParams.get('place_id');

    return placeId;
}


document.addEventListener('DOMContentLoaded', () => {
    const token = getCookie('token');
    checkAuthentication(token);
    const placeId = getPlaceIdFromURL();
    fetchPlaceDetails(token, placeId);
}
);


async function fetchPlaceDetails(token, placeId) {

    const response = await fetch('http://127.0.0.1:6010/api/v1/places', {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        }
    })

    if (response.ok){
        const data = await response.json();
        for(let i = 0; i< data.length; i++){
            if(data[i].id == placeId){
                return displayPlaceDetails(data[i]);
            }
        }
    }else{
        return {"error": 'Not able to fetch place data'};
    }
}
async function displayPlaceDetails(place) {
    const placeDetails = document.querySelector('#place-details');
    placeDetails.textContent = '';
    
    const title = document.createElement('h1');
    title.className = 'heading';
    title.textContent = `${place.title}`;
    placeDetails.append(title);

    let reviewsData = [];
    try {
        reviewsData = await getReviews(place.id); 
        if (!Array.isArray(reviewsData)) {
            throw new Error('Reviews data is not an array');
        }
    } catch (error) {
        console.error('Error fetching reviews:', error.message);
        reviewsData = []; 
    }


    // Add Host, Price, Description, and Amenities
    const host = document.createElement('div');
    host.className = 'host-info';
    host.innerHTML = `<span>Host:</span> John Doe`;

    const price = document.createElement('div');
    price.className = 'price-info';
    price.innerHTML = `<span>Price per night:</span> ${place.price}`;

    const description = document.createElement('div');
    description.className = 'desc-info';
    description.innerHTML = `<span>Description:</span> ${place.description}`;

    const amenities = document.createElement('div');
    amenities.className = 'amenities-info';
    amenities.innerHTML = `<span>Amenities:</span> Wifi, Pool, Air Conditioning`;

    const placeContent = document.createElement('div');
    placeContent.className = 'place-content';
    placeContent.append(host, price, description, amenities);
    placeDetails.append(placeContent);

    const placeReview = document.querySelector('#reviews');
    placeReview.textContent = '';

    const placeHeader = document.createElement('h2');
    placeHeader.textContent = 'Reviews';
    placeReview.append(placeHeader);

    for (let j = 0; j < reviewsData.length; j++) {
        const reviewContent = document.createElement('div');
        reviewContent.className = 'review-content';

        const reviewer = document.createElement('div');
        reviewer.className = 'reviewer';
        reviewer.textContent = 'Name';

        const review = document.createElement('div');
        review.className = 'review';
        review.textContent = `${reviewsData[j].text}`;

        const rating = document.createElement('div');
        rating.className = 'rating';
        rating.textContent = `Rating: ${reviewsData[j].rating}`;

        reviewContent.append(reviewer, review, rating);
        placeReview.append(reviewContent);
    }
}

async function getReviews(id) {
    try {
        const review = await fetch(`http://127.0.0.1:6010/api/v1/reviews/places/${id}/reviews`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (review.ok) {
            const data = await review.json();
            return data;
        } else {
            throw new Error(`Failed to fetch reviews: ${review.status} ${review.statusText}`);
        }
    } catch (error) {
        console.error(error.message);
        return []; 
    }
}