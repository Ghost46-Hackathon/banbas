// Custom JavaScript for Banbas Resort

// TAJ Hotels-style navbar scroll effect
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    const scrollY = window.scrollY;
    
    if (scrollY > 100) {
        // Add scrolled state - becomes white and sticky
        navbar.classList.add('scrolled');
        navbar.classList.add('navbar-sticky');
        navbar.classList.remove('navbar-initial');
    } else {
        // Remove scrolled state - becomes transparent overlay
        navbar.classList.remove('scrolled');
        navbar.classList.remove('navbar-sticky');
        navbar.classList.add('navbar-initial');
    }
});

// Initialize navbar as transparent overlay
document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.navbar');
    navbar.classList.add('navbar-initial');
    
    // Handle logo display
    handleLogoDisplay(navbar);
});

// Handle logo display based on navbar state
function handleLogoDisplay(navbar) {
    const logo = navbar.querySelector('.navbar-logo');
    const fallback = navbar.querySelector('.navbar-fallback');
    
    // Check if logo exists and loads properly
    if (logo) {
        logo.onload = function() {
            fallback.style.display = 'none';
        };
        logo.onerror = function() {
            this.style.display = 'none';
            fallback.style.display = 'inline';
        };
    }
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Gallery filter functionality
document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filter = this.getAttribute('data-filter');
            
            // Update active button
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Filter gallery items
            galleryItems.forEach(item => {
                if (filter === 'all' || item.classList.contains(filter)) {
                    item.style.display = 'block';
                    item.style.animation = 'fadeInUp 0.6s ease-out';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
});

// Animate elements on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in-up');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all cards and sections
document.addEventListener('DOMContentLoaded', function() {
    const elementsToAnimate = document.querySelectorAll('.card, .amenity-card, .section-title');
    elementsToAnimate.forEach(el => {
        observer.observe(el);
    });
});

// Form validation and enhancement
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                // Show error message
                const errorMsg = form.querySelector('.error-message') || document.createElement('div');
                errorMsg.className = 'alert alert-danger error-message mt-3';
                errorMsg.textContent = 'Please fill in all required fields.';
                if (!form.querySelector('.error-message')) {
                    form.appendChild(errorMsg);
                }
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.hasAttribute('required') && !this.value.trim()) {
                    this.classList.add('is-invalid');
                } else {
                    this.classList.remove('is-invalid');
                }
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid') && this.value.trim()) {
                    this.classList.remove('is-invalid');
                }
            });
        });
    });
});

// Image lazy loading for better performance
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
});

// Booking modal functionality (if needed)
function openBookingModal(roomId, roomName) {
    // This would open a booking modal
    console.log(`Opening booking for room ${roomId}: ${roomName}`);
    // Implementation would depend on your booking system
}

// Newsletter subscription
document.addEventListener('DOMContentLoaded', function() {
    const newsletterForm = document.querySelector('#newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            
            // Here you would typically send the email to your backend
            console.log('Newsletter subscription for:', email);
            
            // Show success message
            const successMsg = document.createElement('div');
            successMsg.className = 'alert alert-success mt-3';
            successMsg.textContent = 'Thank you for subscribing to our newsletter!';
            this.appendChild(successMsg);
            
            // Clear form
            this.querySelector('input[type="email"]').value = '';
            
            // Remove success message after 5 seconds
            setTimeout(() => {
                successMsg.remove();
            }, 5000);
        });
    }
});

// Tooltip initialization
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Price calculation for room booking (example)
function calculatePrice(basePrice, nights, guests) {
    let total = basePrice * nights;
    
    // Add extra guest fees
    if (guests > 2) {
        total += (guests - 2) * 25 * nights; // $25 per extra guest per night
    }
    
    return total;
}

// Floating Book Now Button Functionality
document.addEventListener('DOMContentLoaded', function() {
    const floatingBtn = document.querySelector('.floating-book-btn');
    
    if (floatingBtn) {
        // Add click tracking/analytics if needed
        floatingBtn.addEventListener('click', function() {
            // Optional: Add analytics tracking
            console.log('Floating Book Now button clicked');
            
            // The href will handle the navigation
        });
        
        // Hide floating button when scrolled to footer to avoid overlap
        const footer = document.querySelector('footer');
        if (footer) {
            const observer = new IntersectionObserver(function(entries) {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        floatingBtn.style.opacity = '0.5';
                        floatingBtn.style.transform = 'translateY(10px)';
                    } else {
                        floatingBtn.style.opacity = '1';
                        floatingBtn.style.transform = 'translateY(0)';
                    }
                });
            }, { threshold: 0.1 });
            
            observer.observe(footer);
        }
    }
});

// Utility function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Booking form functionality
document.addEventListener('DOMContentLoaded', function() {
    const bookingForm = document.getElementById('booking-form');
    const inquiryForm = document.getElementById('inquiry-form');
    
    if (bookingForm) {
        initializeBookingForm();
    }
    
    if (inquiryForm) {
        initializeInquiryForm();
    }
});

// Initialize booking form functionality
function initializeBookingForm() {
    // Wait for date pickers to be initialized
    setTimeout(() => {
        const checkinInputs = document.querySelectorAll('#quick-checkin, input[name="checkin_date"]');
        const checkoutInputs = document.querySelectorAll('#quick-checkout, input[name="checkout_date"]');
        
        checkinInputs.forEach(input => {
            input.addEventListener('change', updateCheckoutMinDate);
        });
        
        checkoutInputs.forEach(input => {
            input.addEventListener('change', updateBookingSummary);
        });
    }, 100);
    
    // Sync quick booking bar with main form
    document.getElementById('quick-checkin').addEventListener('change', function() {
        document.getElementById('checkin-date').value = this.value;
        updateBookingSummary();
    });
    
    document.getElementById('quick-checkout').addEventListener('change', function() {
        document.getElementById('checkout-date').value = this.value;
        updateBookingSummary();
    });
    
    document.getElementById('quick-guests').addEventListener('change', function() {
        const guestCount = parseInt(this.value);
        document.getElementById('adults').value = Math.min(guestCount, 5);
        updateBookingSummary();
    });
    
    document.getElementById('quick-rooms').addEventListener('change', function() {
        document.getElementById('rooms').value = this.value;
        updateBookingSummary();
    });
    
    // Main form change listeners
    const formInputs = ['adults', 'children', 'rooms', 'room-type'];
    formInputs.forEach(inputId => {
        const element = document.getElementById(inputId);
        if (element) {
            element.addEventListener('change', updateBookingSummary);
        }
    });
    
    // Check availability button
    document.getElementById('check-availability').addEventListener('click', function() {
        const checkin = document.getElementById('quick-checkin').value;
        const checkout = document.getElementById('quick-checkout').value;
        
        if (!checkin || !checkout) {
            alert('Please select both check-in and check-out dates.');
            return;
        }
        
        if (new Date(checkin) >= new Date(checkout)) {
            alert('Check-out date must be after check-in date.');
            return;
        }
        
        // Scroll to main form
        document.querySelector('.main-booking-form').scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
        
        updateBookingSummary();
    });
    
    // Form submission
    document.getElementById('booking-form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (validateBookingForm()) {
            // Show success message
            showBookingSuccess();
        }
    });
    
    // Initial summary update
    updateBookingSummary();
}

// Update minimum checkout date based on checkin
function updateCheckoutMinDate() {
    const checkinDate = this.value;
    if (checkinDate) {
        const minCheckout = new Date(checkinDate);
        minCheckout.setDate(minCheckout.getDate() + 1);
        const minCheckoutStr = minCheckout.toISOString().split('T')[0];
        
        checkoutInputs.forEach(input => {
            input.min = minCheckoutStr;
        });
    }
}

// Update booking summary
function updateBookingSummary() {
    // Try to get values from both regular inputs and hidden inputs
    const checkin = document.querySelector('input[name="checkin_date"]')?.value || document.getElementById('checkin-date')?.value;
    const checkout = document.querySelector('input[name="checkout_date"]')?.value || document.getElementById('checkout-date')?.value;
    const adults = parseInt(document.getElementById('adults')?.value) || 0;
    const children = parseInt(document.getElementById('children')?.value) || 0;
    const rooms = parseInt(document.getElementById('rooms')?.value) || 1;
    const roomType = document.getElementById('room-type')?.value;
    
    // Update summary display
    document.getElementById('summary-checkin').textContent = checkin ? formatDate(checkin) : '-';
    document.getElementById('summary-checkout').textContent = checkout ? formatDate(checkout) : '-';
    document.getElementById('summary-guests').textContent = adults + children > 0 ? `${adults + children} guests` : '-';
    document.getElementById('summary-rooms').textContent = rooms > 0 ? `${rooms} room${rooms > 1 ? 's' : ''}` : '-';
    
    // Calculate nights and pricing
    if (checkin && checkout) {
        const checkinDate = new Date(checkin);
        const checkoutDate = new Date(checkout);
        const nights = Math.ceil((checkoutDate - checkinDate) / (1000 * 60 * 60 * 24));
        
        if (nights > 0) {
            document.getElementById('summary-nights').textContent = `${nights} night${nights > 1 ? 's' : ''}`;
            
            // Base room rates by type
            const rates = {
                '': 299,
                'deluxe': 399,
                'suite': 599,
                'oceanview': 699,
                'presidential': 1299
            };
            
            const baseRate = rates[roomType] || 299;
            const totalRoomCost = baseRate * nights * rooms;
            const taxesAndFees = Math.round(totalRoomCost * 0.15); // 15% taxes and fees
            const grandTotal = totalRoomCost + taxesAndFees;
            
            document.getElementById('summary-rate').textContent = formatCurrency(baseRate);
            document.getElementById('summary-total').textContent = formatCurrency(totalRoomCost);
            document.getElementById('summary-taxes').textContent = formatCurrency(taxesAndFees);
            document.getElementById('summary-grand-total').textContent = formatCurrency(grandTotal);
        } else {
            document.getElementById('summary-nights').textContent = '-';
            resetPricingDisplay();
        }
    } else {
        document.getElementById('summary-nights').textContent = '-';
        resetPricingDisplay();
    }
}

// Reset pricing display
function resetPricingDisplay() {
    document.getElementById('summary-total').textContent = '$0';
    document.getElementById('summary-taxes').textContent = '$0';
    document.getElementById('summary-grand-total').textContent = '$0';
}

// Format date for display
function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
        weekday: 'short',
        month: 'short',
        day: 'numeric',
        year: 'numeric'
    });
}

// Validate booking form
function validateBookingForm() {
    const requiredFields = [
        'first-name', 'last-name', 'email', 'phone',
        'checkin-date', 'checkout-date', 'adults', 'rooms'
    ];
    
    let isValid = true;
    const errors = [];
    
    // Check required fields
    requiredFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field && !field.value.trim()) {
            isValid = false;
            field.classList.add('is-invalid');
            errors.push(`${field.previousElementSibling.textContent.replace('*', '')} is required`);
        } else if (field) {
            field.classList.remove('is-invalid');
        }
    });
    
    // Validate dates
    const checkin = document.getElementById('checkin-date').value;
    const checkout = document.getElementById('checkout-date').value;
    
    if (checkin && checkout) {
        const checkinDate = new Date(checkin);
        const checkoutDate = new Date(checkout);
        
        if (checkinDate >= checkoutDate) {
            isValid = false;
            document.getElementById('checkout-date').classList.add('is-invalid');
            errors.push('Check-out date must be after check-in date');
        }
        
        if (checkinDate < new Date().setHours(0,0,0,0)) {
            isValid = false;
            document.getElementById('checkin-date').classList.add('is-invalid');
            errors.push('Check-in date cannot be in the past');
        }
    }
    
    // Validate email format
    const email = document.getElementById('email').value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (email && !emailRegex.test(email)) {
        isValid = false;
        document.getElementById('email').classList.add('is-invalid');
        errors.push('Please enter a valid email address');
    }
    
    // Show errors if any
    if (!isValid) {
        let errorDiv = document.querySelector('.booking-error-message');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'alert alert-danger booking-error-message mt-3';
            document.querySelector('#booking-form').appendChild(errorDiv);
        }
        errorDiv.innerHTML = `<strong>Please fix the following errors:</strong><ul class="mb-0 mt-2">${errors.map(error => `<li>${error}</li>`).join('')}</ul>`;
        
        // Scroll to first error
        const firstError = document.querySelector('.is-invalid');
        if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    } else {
        // Remove error message if exists
        const errorDiv = document.querySelector('.booking-error-message');
        if (errorDiv) {
            errorDiv.remove();
        }
    }
    
    return isValid;
}

// Show booking success message
function showBookingSuccess() {
    const formContainer = document.querySelector('.booking-form-container');
    const successHtml = `
        <div class="text-center py-5">
            <div class="success-animation mb-4">
                <i class="fas fa-check-circle text-success" style="font-size: 4rem;"></i>
            </div>
            <h2 class="text-success mb-3">Booking Request Submitted!</h2>
            <p class="lead mb-4">Thank you for choosing Banbas Resort. We've received your booking request and will contact you within 24 hours to confirm availability and finalize your reservation.</p>
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">What happens next?</h5>
                            <div class="row text-start">
                                <div class="col-md-6">
                                    <p><i class="fas fa-phone text-primary me-2"></i><strong>We'll call you</strong><br>Our reservations team will contact you to confirm details</p>
                                </div>
                                <div class="col-md-6">
                                    <p><i class="fas fa-envelope text-primary me-2"></i><strong>Email confirmation</strong><br>You'll receive a detailed booking confirmation</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="mt-4">
                <a href="/" class="btn btn-primary me-3">Return to Home</a>
                <button onclick="location.reload()" class="btn btn-outline-primary">Make Another Booking</button>
            </div>
        </div>
    `;
    
    formContainer.innerHTML = successHtml;
    
    // Scroll to success message
    formContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Initialize inquiry form
function initializeInquiryForm() {
    document.getElementById('inquiry-form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const name = this.querySelector('input[name="inquiry_name"]').value;
        const email = this.querySelector('input[name="inquiry_email"]').value;
        const message = this.querySelector('textarea[name="inquiry_message"]').value;
        
        if (!name || !email || !message) {
            alert('Please fill in all fields.');
            return;
        }
        
        // Show success message
        showInquirySuccess(this);
    });
}

// Show inquiry success message
function showInquirySuccess(form) {
    const successMsg = document.createElement('div');
    successMsg.className = 'alert alert-success mt-3';
    successMsg.innerHTML = `
        <i class="fas fa-check-circle me-2"></i>
        <strong>Message sent successfully!</strong> We'll get back to you within 24 hours.
    `;
    
    form.appendChild(successMsg);
    form.reset();
    
    // Remove success message after 5 seconds
    setTimeout(() => {
        successMsg.remove();
    }, 5000);
}

// Enhanced contact form functionality
document.addEventListener('DOMContentLoaded', function() {
    const inquiryTypeSelect = document.getElementById('inquiry-type');
    const bookingCheckin = document.getElementById('booking-checkin');
    
    if (inquiryTypeSelect && bookingCheckin) {
        // Set minimum date for check-in
        const today = new Date().toISOString().split('T')[0];
        const checkinInput = document.getElementById('preferred-checkin') || document.getElementById('id_preferred_checkin');
        if (checkinInput) {
            checkinInput.min = today;
        }
        
        // Initialize visibility on load
        const toggleBooking = () => {
            if (inquiryTypeSelect.value === 'booking') {
                bookingCheckin.classList.remove('d-none');
                bookingCheckin.style.animation = 'fadeInUp 0.3s ease-out';
                // If no date chosen yet, default to today for convenience
                if (checkinInput && !checkinInput.value) {
                    checkinInput.value = today;
                }
            } else {
                bookingCheckin.classList.add('d-none');
            }
        };
        toggleBooking();
        
        // Show/hide check-in based on inquiry type
        inquiryTypeSelect.addEventListener('change', toggleBooking);
    }
});

// Add booking inquiry section styles
const bookingInquirySectionStyles = `
.booking-inquiry-section {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-radius: 15px;
    padding: 25px;
    border: 2px solid rgba(0, 102, 204, 0.1);
    margin-top: 1rem;
}

.booking-inquiry-section h5 {
    font-family: var(--font-display);
    margin-bottom: 1rem;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
`;

// Inject styles if not already present
if (!document.getElementById('booking-inquiry-styles')) {
    const styleSheet = document.createElement('style');
    styleSheet.id = 'booking-inquiry-styles';
    styleSheet.textContent = bookingInquirySectionStyles;
    document.head.appendChild(styleSheet);
}

// Modern Date Picker Implementation
class ModernDatePicker {
    constructor(element, options = {}) {
        this.element = element;
        this.options = {
            format: 'YYYY-MM-DD',
            minDate: new Date(),
            maxDate: null,
            placeholder: 'Select date',
            showQuickDates: true,
            closeOnSelect: true,
            rangeMode: false,
            ...options
        };
        
        this.currentDate = new Date();
        this.selectedDate = null;
        this.rangeStart = null;
        this.rangeEnd = null;
        this.isOpen = false;
        
        this.init();
    }
    
    init() {
        this.createHTML();
        this.bindEvents();
        this.render();
    }
    
    createHTML() {
        // Create wrapper
        this.wrapper = document.createElement('div');
        this.wrapper.className = 'custom-date-picker';
        
        // Create hidden input for form submission (keep original element)
        this.hiddenInput = this.element;
        this.hiddenInput.type = 'hidden';
        
        // Create display input
        this.input = document.createElement('input');
        this.input.type = 'text';
        this.input.className = 'date-picker-input';
        this.input.placeholder = this.options.placeholder;
        this.input.readOnly = true;
        
        // Create icon
        this.icon = document.createElement('i');
        this.icon.className = 'fas fa-calendar-alt date-picker-icon';
        
        // Create calendar
        this.calendar = document.createElement('div');
        this.calendar.className = 'date-picker-calendar';
        this.calendar.innerHTML = this.getCalendarHTML();
        
        // Assemble
        this.wrapper.appendChild(this.icon);
        this.wrapper.appendChild(this.input);
        this.wrapper.appendChild(this.hiddenInput);
        this.wrapper.appendChild(this.calendar);
        
        // Replace original element
        this.element.parentNode.replaceChild(this.wrapper, this.element);
    }
    
    getCalendarHTML() {
        return `
            <div class="calendar-header">
                <button type="button" class="calendar-nav-button" data-action="prev-month">
                    <i class="fas fa-chevron-left"></i>
                </button>
                <div class="calendar-title"></div>
                <button type="button" class="calendar-nav-button" data-action="next-month">
                    <i class="fas fa-chevron-right"></i>
                </button>
            </div>
            <div class="calendar-grid">
                <div class="calendar-day-header">Sun</div>
                <div class="calendar-day-header">Mon</div>
                <div class="calendar-day-header">Tue</div>
                <div class="calendar-day-header">Wed</div>
                <div class="calendar-day-header">Thu</div>
                <div class="calendar-day-header">Fri</div>
                <div class="calendar-day-header">Sat</div>
            </div>
            <div class="calendar-footer">
                <button type="button" class="calendar-today-button">Today</button>
                <button type="button" class="calendar-clear-button">Clear</button>
            </div>
            ${this.options.showQuickDates ? this.getQuickDatesHTML() : ''}
        `;
    }
    
    getQuickDatesHTML() {
        return `
            <div class="quick-dates">
                <div class="quick-dates-title">Quick Select</div>
                <div class="quick-date-buttons">
                    <button type="button" class="quick-date-btn" data-days="0">Today</button>
                    <button type="button" class="quick-date-btn" data-days="1">Tomorrow</button>
                    <button type="button" class="quick-date-btn" data-days="7">Next Week</button>
                    <button type="button" class="quick-date-btn" data-days="30">Next Month</button>
                </div>
            </div>
        `;
    }
    
    bindEvents() {
        // Input click
        this.input.addEventListener('click', () => this.toggle());
        
        // Calendar events
        this.calendar.addEventListener('click', (e) => this.handleCalendarClick(e));
        
        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!this.wrapper.contains(e.target)) {
                this.close();
            }
        });
        
        // Keyboard navigation
        this.input.addEventListener('keydown', (e) => this.handleKeydown(e));
    }
    
    handleCalendarClick(e) {
        const action = e.target.dataset.action;
        const day = e.target.dataset.day;
        const quickDays = e.target.dataset.days;
        
        if (action === 'prev-month') {
            this.currentDate.setMonth(this.currentDate.getMonth() - 1);
            this.render();
        } else if (action === 'next-month') {
            this.currentDate.setMonth(this.currentDate.getMonth() + 1);
            this.render();
        } else if (day) {
            this.selectDate(new Date(this.currentDate.getFullYear(), this.currentDate.getMonth(), parseInt(day)));
        } else if (e.target.classList.contains('calendar-today-button')) {
            this.selectDate(new Date());
        } else if (e.target.classList.contains('calendar-clear-button')) {
            this.clear();
        } else if (quickDays !== undefined) {
            const date = new Date();
            date.setDate(date.getDate() + parseInt(quickDays));
            this.selectDate(date);
        }
    }
    
    handleKeydown(e) {
        if (e.key === 'Escape') {
            this.close();
        } else if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            this.toggle();
        }
    }
    
    selectDate(date) {
        if (this.isDateDisabled(date)) return;
        
        this.selectedDate = new Date(date);
        const formattedDate = this.formatDate(date);
        
        // Update display input
        this.input.value = this.formatDisplayDate(date);
        
        // Update hidden input for form submission
        this.hiddenInput.value = formattedDate;
        
        // Add animation
        const dayElement = this.calendar.querySelector(`[data-day="${date.getDate()}"]`);
        if (dayElement) {
            dayElement.classList.add('animate-select');
            setTimeout(() => dayElement.classList.remove('animate-select'), 300);
        }
        
        // Trigger change event on hidden input
        this.hiddenInput.dispatchEvent(new Event('change', { bubbles: true }));
        
        if (this.options.closeOnSelect) {
            setTimeout(() => this.close(), 150);
        }
        
        this.render();
    }
    
    clear() {
        this.selectedDate = null;
        this.input.value = '';
        this.hiddenInput.value = '';
        this.hiddenInput.dispatchEvent(new Event('change', { bubbles: true }));
        this.render();
    }
    
    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }
    
    open() {
        this.isOpen = true;
        this.calendar.classList.add('show');
        
        // Reset to selected date or today
        if (this.selectedDate) {
            this.currentDate = new Date(this.selectedDate);
        } else {
            this.currentDate = new Date();
        }
        
        this.render();
    }
    
    close() {
        this.isOpen = false;
        this.calendar.classList.remove('show');
    }
    
    render() {
        this.renderTitle();
        this.renderDays();
    }
    
    renderTitle() {
        const title = this.calendar.querySelector('.calendar-title');
        const monthNames = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ];
        
        title.textContent = `${monthNames[this.currentDate.getMonth()]} ${this.currentDate.getFullYear()}`;
    }
    
    renderDays() {
        const grid = this.calendar.querySelector('.calendar-grid');
        const daysHeader = grid.querySelectorAll('.calendar-day-header');
        
        // Remove existing day buttons
        grid.querySelectorAll('.calendar-day').forEach(day => day.remove());
        
        const firstDay = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth(), 1);
        const lastDay = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() + 1, 0);
        const startDate = new Date(firstDay);
        startDate.setDate(startDate.getDate() - firstDay.getDay());
        
        for (let i = 0; i < 42; i++) {
            const date = new Date(startDate);
            date.setDate(startDate.getDate() + i);
            
            const dayButton = document.createElement('button');
            dayButton.type = 'button';
            dayButton.className = 'calendar-day';
            dayButton.textContent = date.getDate();
            dayButton.dataset.day = date.getDate();
            
            // Add classes
            if (date.getMonth() !== this.currentDate.getMonth()) {
                dayButton.classList.add('other-month');
            }
            
            if (this.isToday(date)) {
                dayButton.classList.add('today');
            }
            
            if (this.isDateDisabled(date)) {
                dayButton.classList.add('disabled');
                dayButton.disabled = true;
            }
            
            if (this.selectedDate && this.isSameDay(date, this.selectedDate)) {
                dayButton.classList.add('selected');
            }
            
            grid.appendChild(dayButton);
        }
    }
    
    isToday(date) {
        const today = new Date();
        return this.isSameDay(date, today);
    }
    
    isSameDay(date1, date2) {
        return date1.getDate() === date2.getDate() &&
               date1.getMonth() === date2.getMonth() &&
               date1.getFullYear() === date2.getFullYear();
    }
    
    isDateDisabled(date) {
        if (this.options.minDate && date < this.options.minDate) {
            return true;
        }
        if (this.options.maxDate && date > this.options.maxDate) {
            return true;
        }
        return false;
    }
    
    formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        
        switch (this.options.format) {
            case 'DD/MM/YYYY':
                return `${day}/${month}/${year}`;
            case 'MM/DD/YYYY':
                return `${month}/${day}/${year}`;
            case 'YYYY-MM-DD':
            default:
                return `${year}-${month}-${day}`;
        }
    }
    
    formatDisplayDate(date) {
        const monthNames = [
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ];
        const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        
        const dayName = dayNames[date.getDay()];
        const day = date.getDate();
        const month = monthNames[date.getMonth()];
        const year = date.getFullYear();
        
        return `${dayName}, ${month} ${day}, ${year}`;
    }
    
    getValue() {
        return this.selectedDate;
    }
    
    setValue(date) {
        if (date) {
            this.selectDate(new Date(date));
        } else {
            this.clear();
        }
    }
}

// Initialize modern date pickers on booking form
document.addEventListener('DOMContentLoaded', function() {
    // Replace date inputs with modern date pickers
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const datePickers = [];
    
    dateInputs.forEach((input, index) => {
        const isCheckout = input.id && input.id.includes('checkout');
        const minDate = new Date();
        
        // Set minimum date for checkout to be tomorrow if it's the checkout field
        if (isCheckout) {
            minDate.setDate(minDate.getDate() + 1);
        }
        
        const picker = new ModernDatePicker(input, {
            placeholder: isCheckout ? 'Select check-out date' : 'Select check-in date',
            minDate: minDate,
            showQuickDates: true,
            format: 'YYYY-MM-DD'
        });
        
        datePickers.push({ picker, isCheckout });
    });
    
    // Link check-in and check-out date pickers
    if (datePickers.length >= 2) {
        const checkinPicker = datePickers.find(dp => !dp.isCheckout);
        const checkoutPicker = datePickers.find(dp => dp.isCheckout);
        
        if (checkinPicker && checkoutPicker) {
            checkinPicker.picker.input.addEventListener('change', function() {
                const checkinDate = checkinPicker.picker.getValue();
                if (checkinDate) {
                    const minCheckoutDate = new Date(checkinDate);
                    minCheckoutDate.setDate(minCheckoutDate.getDate() + 1);
                    checkoutPicker.picker.options.minDate = minCheckoutDate;
                    
                    // Clear checkout if it's before the new minimum
                    const checkoutDate = checkoutPicker.picker.getValue();
                    if (checkoutDate && checkoutDate <= checkinDate) {
                        checkoutPicker.picker.clear();
                    }
                }
            });
        }
    }
});

// Utility function to create date picker
function createDatePicker(selector, options = {}) {
    const elements = document.querySelectorAll(selector);
    const pickers = [];
    
    elements.forEach(element => {
        pickers.push(new ModernDatePicker(element, options));
    });
    
    return pickers.length === 1 ? pickers[0] : pickers;
}
