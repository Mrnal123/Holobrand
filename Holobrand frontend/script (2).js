// At the top of your file, import the config
import config from './config.js';

window.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector('.container');

  container.addEventListener('animationend', () => {
    console.log("Animation complete ✅");
  });
   
  // Add event listener to the Generate Layout button
  document.getElementById('generateLayoutBtn').addEventListener('click', submitForm);
});

// Export submitForm to make it globally available
window.submitForm = async function submitForm() {
  const formData = new FormData();
  const imageInput = document.getElementById('productImage');
  const resultMessage = document.getElementById('resultMessage');
  const loader = document.getElementById('loader');
  const button = document.querySelector('button');

  if (!imageInput.files.length) {
    alert('Please upload a product image.');
    return;
  }

  formData.append('image', imageInput.files[0]);
  formData.append('brand_color', document.getElementById('brandColor').value); // Changed to match backend
  formData.append('font', document.getElementById('brandFont').value);
  formData.append('style_prompt', document.getElementById('brandPrompt').value); // Changed to match backend
  formData.append('preview_mode', document.getElementById('previewMode').value); // Changed to match backend

  resultMessage.textContent = '';
  loader.style.display = 'block';
  button.disabled = true;
  button.textContent = 'Generating...';

  try {
    // Use the config.apiUrl and change to the endpoint that exists in your Flask app
    const response = await fetch(`${config.apiUrl}/api/generate-layout`, {
      method: 'POST',
      body: formData
      // No need to set Content-Type header as the browser will set it correctly for FormData
    });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const result = await response.json();
    console.log('Server response:', result);

    if (result.status === 'generated' || result.layout) { // Added check for layout
      resultMessage.textContent = 'Layout generated successfully! Opening preview...';
      // Store the layout data in sessionStorage so it can be accessed by the preview page
      sessionStorage.setItem('generatedLayout', JSON.stringify(result));
      setTimeout(() => window.open(`${config.apiUrl}/preview`, '_blank'), 1000);
    } else {
      resultMessage.textContent = 'Generation failed. Please try again.';
    }
  } catch (error) {
    console.error('Error:', error);
    resultMessage.textContent = 'Error occurred during generation.';
  } finally {
    loader.style.display = 'none';
    button.disabled = false;
    button.textContent = 'Generate Layout';
  }
}
