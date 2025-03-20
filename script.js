document.addEventListener('DOMContentLoaded', function() {
    // About modal functionality
    const aboutLink = document.querySelector('.nav-menu li:nth-child(3) a');
    const aboutModal = document.getElementById('aboutModal');
    const closeModal = document.querySelector('.close-modal');
    
    if (aboutLink && aboutModal) {
        aboutLink.addEventListener('click', function(e) {
            e.preventDefault();
            aboutModal.classList.add('active');
        });
    }
    
    if (closeModal && aboutModal) {
        closeModal.addEventListener('click', function() {
            aboutModal.classList.remove('active');
        });
        
        // Close modal when clicking outside the modal content
        aboutModal.addEventListener('click', function(e) {
            if (e.target === aboutModal) {
                aboutModal.classList.remove('active');
            }
        });
    }
    
    // Mobile menu toggle functionality
    const menuToggle = document.getElementById('menuToggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
    
    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        if (!event.target.closest('nav') && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
        }
    });
    
    // Initialize OpenStreetMap
    const mapElement = document.getElementById('map');
    let map;
    let userMarker;
    
    if (mapElement) {
        // Initialize the map with a default view of Bangladesh
        map = L.map('map').setView([23.8103, 90.4125], 7);
        
        // Add OpenStreetMap tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 19
        }).addTo(map);
    }
    
    // Current location button functionality
    const locationBtn = document.getElementById('currentLocation');
    if (locationBtn) {
        locationBtn.addEventListener('click', function() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    const lat = position.coords.latitude;
                    const lng = position.coords.longitude;
                    
                    // Center map on user's location
                    map.setView([lat, lng], 15);
                    
                    // Add or update marker for user's location
                    if (userMarker) {
                        userMarker.setLatLng([lat, lng]);
                    } else {
                        userMarker = L.marker([lat, lng]).addTo(map);
                        userMarker.bindPopup('Your location').openPopup();
                    }
                }, function(error) {
                    console.error('Error getting location:', error);
                    alert('Unable to get your location. Please check your permissions.');
                });
            } else {
                alert('Geolocation is not supported by your browser.');
            }
        });
    }
    
    // Report button functionality
    const reportBtn = document.getElementById('reportBtn');
    if (reportBtn) {
        reportBtn.addEventListener('click', function() {
            // Placeholder for report functionality
            alert('Report functionality will be implemented here');
        });
    }
});