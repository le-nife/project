
document.addEventListener('DOMContentLoaded', () => {

    const flashMessages = document.querySelectorAll('[class*="flash"]');

    flashMessages.forEach((message) => {
        const displayDuration = 5000;

        setTimeout(() => {
        
            message.style.transition = "opacity 0.6s ease, margin-top 0.6s ease, mb-0.6s ease";
            message.style.opacity = "0";
            
            
            setTimeout(() => {
                if (message.parentNode) {
                    message.remove();
                }
            }, 600);

        }, displayDuration);
    });
});