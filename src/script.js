document.addEventListener('DOMContentLoaded', function() {
    // Modal elements
    const loginBtn = document.getElementById('loginBtn');
    const signupBtn = document.getElementById('signupBtn');
    const loginModal = document.getElementById('loginModal');
    const signupModal = document.getElementById('signupModal');
    const closeModalBtns = document.querySelectorAll('.close-modal');
    const switchToSignup = document.getElementById('switchToSignup');
    
    // Form elements
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    const newsletterForm = document.getElementById('newsletterForm');
    const uploadBox = document.getElementById('uploadBox');
    
    // Open Login Modal
    loginBtn.addEventListener('click', function(e) {
        e.preventDefault();
        loginModal.style.display = 'block';
    });
    
    // Open Signup Modal
    signupBtn.addEventListener('click', function(e) {
        e.preventDefault();
        signupModal.style.display = 'block';
    });
    
    // Close Modals
    closeModalBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            loginModal.style.display = 'none';
            signupModal.style.display = 'none';
        });
    });
    
    // Switch to Signup from Login
    switchToSignup.addEventListener('click', function(e) {
        e.preventDefault();
        loginModal.style.display = 'none';
        signupModal.style.display = 'block';
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === loginModal) {
            loginModal.style.display = 'none';
        }
        if (e.target === signupModal) {
            signupModal.style.display = 'none';
        }
    });
    
    // Login Form Submission
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        // Add your login logic here
        alert('Login functionality will be implemented here');
        loginModal.style.display = 'none';
    });
    
    // Signup Form Submission
    signupForm.addEventListener('submit', function(e) {
        e.preventDefault();
        // Add your signup logic here
        alert('Signup functionality will be implemented here');
        signupModal.style.display = 'none';
    });
    
    // Newsletter Form Submission
    newsletterForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const email = newsletterForm.querySelector('input[type="email"]').value;
        // Add your newsletter subscription logic here
        alert(`Thank you for subscribing with ${email}`);
        newsletterForm.reset();
    });
    
    // File Upload Handling
    uploadBox.addEventListener('click', function() {
        // This would trigger a file input in a real implementation
        alert('File upload functionality will be implemented here');
    });
    
    // Drag and Drop for File Upload
    uploadBox.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.style.borderColor = getComputedStyle(document.documentElement).getPropertyValue('--secondary');  // ✅ Correct

    });
    
    uploadBox.addEventListener('dragleave', function() {
        this.style.borderColor = '#ccc';
    });
    
    uploadBox.addEventListener('drop', function(e) {
        e.preventDefault();
        this.style.borderColor = '#ccc';
        // Handle dropped files
        alert('File drop functionality will be implemented here');
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                document.querySelector(targetId).scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});