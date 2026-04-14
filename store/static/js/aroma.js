const cert = document.getElementById('cert-preview');
const modal = document.getElementById('cert-modal');

if (cert && modal) {
    cert.addEventListener('click', () => {
        modal.classList.add('active');
    });

    modal.addEventListener('click', () => {
        modal.classList.remove('active');
    });
}