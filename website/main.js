// Intersection Observer for Scroll Animations
const observerOptions = {
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('active');
        }
    });
}, observerOptions);

document.addEventListener('DOMContentLoaded', () => {
    const revealElements = document.querySelectorAll('.reveal');
    revealElements.forEach(el => observer.observe(el));
    initDemo();
});

// Smooth Scroll for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Interactive Demo Logic
function initDemo() {
    const shortenBtn = document.getElementById('shorten-btn');
    const targetInput = document.getElementById('target-url');
    const demoStatus = document.getElementById('demo-status');
    const demoResult = document.getElementById('demo-result');
    const resultLink = document.getElementById('result-link');
    const resetBtn = document.getElementById('reset-demo');
    const statusSteps = document.querySelectorAll('.status-step');

    if (!shortenBtn) return;

    shortenBtn.addEventListener('click', async () => {
        const url = targetInput.value.trim();
        if (!url) {
            alert("Please enter a URL to shorten");
            return;
        }

        // Reset UI
        shortenBtn.disabled = true;
        demoStatus.style.display = 'flex';
        demoResult.classList.add('hidden');
        statusSteps.forEach(s => s.classList.remove('active'));

        // Simulate Backend Flow
        const steps = ['step-validate', 'step-hash', 'step-collision', 'step-persist'];

        for (const stepId of steps) {
            const step = document.getElementById(stepId);
            step.classList.add('active');
            await new Promise(r => setTimeout(r, 800)); // Simulate processing time
        }

        // Finalize Result
        const mockHash = Math.random().toString(36).substring(2, 8);
        const shortUrl = `http://hr.io/${mockHash}`;
        resultLink.textContent = shortUrl;
        resultLink.style.cursor = 'pointer';
        resultLink.title = 'Click to simulate redirect';

        demoStatus.style.display = 'none';
        demoResult.classList.remove('hidden');
        shortenBtn.disabled = false;

        // Add simulated redirect handler
        resultLink.onclick = () => {
            alert(`[HashRoute Simulation]\n\nRedirecting from: ${shortUrl}\nTo: ${url}\n\nStatus: 307 Temporary Redirect`);
        };
    });

    const copyBtn = document.getElementById('copy-btn');
    copyBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(resultLink.textContent);
        const originalText = copyBtn.textContent;
        copyBtn.textContent = 'Copied!';
        setTimeout(() => {
            copyBtn.textContent = originalText;
        }, 2000);
    });

    resetBtn.addEventListener('click', () => {
        targetInput.value = '';
        demoResult.classList.add('hidden');
        demoStatus.style.display = 'none';
        shortenBtn.disabled = false;
    });
}
