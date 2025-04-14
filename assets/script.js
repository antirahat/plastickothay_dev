

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
            // Check if the menu toggle is already active (X state)
            if (menuToggle.classList.contains('active')) {
                // If it's active (X showing), hide the menu
                navMenu.classList.remove('active');
                menuToggle.classList.remove('active');
            } else {
                // If it's not active (hamburger showing), show the menu
                navMenu.classList.add('active');
                menuToggle.classList.add('active');
            }
        });
    }
    
    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        if (!event.target.closest('nav') && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
            menuToggle.classList.remove('active');
        }
    });
    
    // Initialize OpenStreetMap
    const mapElement = document.getElementById('map');
    let map;
    let userMarker;
    
    if (mapElement) {
        // Initialize the map with a default view of Bangladesh
        map = L.map('map'); // do not use setview initially 
        
        // Add OpenStreetMap tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 18
        }).addTo(map);
        connectLocation();
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

    //connect location function
    function connectLocation() {
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
            
        }   // Add or update marker for user's location
    }

    document.querySelector('.profile-btn').addEventListener('click', () => {
        document.querySelector('.profile-modal').classList.add('active');
    });
    
    // Profile modal close functionality
    const profileModal = document.querySelector('.profile-modal');
    const profileCloseModal = profileModal ? profileModal.querySelector('.close-modal') : null;
    
    if (profileCloseModal && profileModal) {
        profileCloseModal.addEventListener('click', function() {
            profileModal.classList.remove('active');
        });
        
        // Close modal when clicking outside the modal content
        profileModal.addEventListener('click', function(e) {
            if (e.target === profileModal) {
                profileModal.classList.remove('active');
            }
        });
    }
    
    // Tab switching
    const authTabs = document.querySelectorAll('.auth-tab');
    authTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            authTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            // Toggle form fields and button text based on active tab
        });
    });

    // Sign up and sign in functionality
    const signUpForm = document.getElementById('signUpForm');
    const signInForm = document.getElementById('signInForm');
    // Report button functionality
    const reportBtn = document.getElementById('reportBtn');
    const reportModal = document.getElementById('reportModal');
    const reportCloseModal = reportModal ? reportModal.querySelector('.close-modal') : null;
    const photoInput = document.getElementById('photo');
    const photoPreview = document.getElementById('photoPreview');
    const reportForm = document.getElementById('reportForm');
    const openphotoBtn = document.getElementById('openphotoBtn');
    const photoModal = document.getElementById('photoModal');
    const photoCloseModal = photoModal ? photoModal.querySelector('.close-modal') : null;
    
    if (reportBtn && reportModal) {
        reportBtn.addEventListener('click', function() {
            reportModal.classList.add('active');
        });
    }
    
    if (reportCloseModal && reportModal) {
        reportCloseModal.addEventListener('click', function() {
            reportModal.classList.remove('active');
        });
        
        // Close modal when clicking outside the modal content
        reportModal.addEventListener('click', function(e) {
            if (e.target === reportModal) {
                reportModal.classList.remove('active');
            }
        });
    }
    
    // Photo preview functionality
    if (photoInput && photoPreview) {
        photoInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    photoPreview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
                }
                
                reader.readAsDataURL(this.files[0]);
            } else {
                photoPreview.innerHTML = '';
            }
        });
    }
    
    // Form submission
    if (reportForm) {
        reportForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this);
            const reportData = {
                name: formData.get('name'),
                severity: formData.get('severity'),
                phone: formData.get('phone'),
                email: formData.get('email'),
                photo: photoInput.files[0] ? photoInput.files[0].name : null
            };
            
            // For now, just log the data and show success message
            console.log('Report submitted:', reportData);
            alert('Thank you for your report! We will review it shortly.');
            
            // Reset form and close modal
            this.reset();
            photoPreview.innerHTML = '';
            reportModal.classList.remove('active');
            
            // In a real application, you would send this data to a server
            // using fetch or XMLHttpRequest
        });
    }

    // photo modal control
if (openphotoBtn && photoModal) {
    openphotoBtn.addEventListener('click', function() {
        openphotoBtn.classList.add('active');
    });
}

if (photoCloseModal && photoModal) {
    photoCloseModal.addEventListener('click', function() {
        photoModal.classList.remove('active');
    });
    
    // Close modal when clicking outside the modal content
    photoModal.addEventListener('click', function(e) {
        if (e.target === reportModal) {
            photoModal.classList.remove('active');
        }
    });
}

// const video = document.getElementById('video');
//         const canvas = document.getElementById('canvas');
//         const photo = document.getElementById('photo');
//         const capture = document.getElementById('capture');
    
//         // Ask for camera access
//         navigator.mediaDevices.getUserMedia({ video: true })
//           .then((stream) => {
//             video.srcObject = stream;
//           })
//           .catch((err) => {
//             console.error("Error accessing camera:", err);
//             alert("Camera access denied or not available.");
//           });
    
//         // Capture photo on button click
//         capture.addEventListener('click', () => {
//           const context = canvas.getContext('2d');
//           context.drawImage(video, 0, 0, canvas.width, canvas.height);
//           const dataURL = canvas.toDataURL('image/png');
//           photo.src = dataURL;
//         });
});