    $(document).ready(function() {
        $('.star-rating .star').on('click', function() {
            var ratingValue = $(this).data('value');
            var $ratingInput = $(this).closest('.star-rating').find('input[name="rating"]');
            $ratingInput.val(ratingValue);
            updateStarRating($(this).closest('.star-rating'), ratingValue);
        });

        function updateStarRating($ratingContainer, ratingValue) {
            $ratingContainer.find('.star').each(function() {
                var currentValue = $(this).data('value');
                if (currentValue <= ratingValue) {
                    $(this).addClass('fas');
                    $(this).removeClass('far');
                } else {
                    $(this).addClass('far');
                    $(this).removeClass('fas');
                }
            });
        }
    });
// Get the SVG element
const svgElement = document.querySelector('svg');

// Define the animation function
function animate() {
  // Reset the animation by removing the 'animated' class
  svgElement.classList.remove('animated');

  // Trigger reflow to restart the animation
  void svgElement.offsetWidth;

  // Add the 'animated' class to start the animation
  svgElement.classList.add('animated');
}

// Trigger the animation when the page loads
window.addEventListener('load', animate);

// Listen for animation end event
svgElement.addEventListener('animationend', () => {
  // Remove the 'animated' class to reset the animation
  svgElement.classList.remove('animated');
});
    $(document).ready(function () {
        $('#hotelPicturesCarousel').carousel();
    });