$(document).ready(function() {
  // Star rating functionality
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

  // SVG animation
  const svgElement = document.querySelector('svg');

  function animate() {
    svgElement.classList.remove('animated');
    void svgElement.offsetWidth;
    svgElement.classList.add('animated');
  }

  window.addEventListener('load', animate);

  svgElement.addEventListener('animationend', () => {
    svgElement.classList.remove('animated');
  });

  // Carousel initialization
  $('#hotelPicturesCarousel').carousel();

  // Room form submission
  $('#roomForm').submit(function(event) {
    event.preventDefault();

    var roomNumber = $('#roomNumberInput').val();
    var roomCapacity = $('#roomCapacityInput').val();
    var roomPrice = $('#roomPriceInput').val();

    var formData = {
      room_number: roomNumber,
      room_capacity: roomCapacity,
      room_price: roomPrice
    };

    $.ajax({
      url: $(this).attr('action'),
      type: 'POST',
      data: formData,
      dataType: 'json',
      success: function(response) {
        console.log('Room details updated successfully');
        $('#roomModal').modal('hide');
      },
      error: function(xhr, status, error) {
        console.log('Error updating room details:', error);
      }
    });
  });

  // AJAX request for updating room availability
  $.ajax({
    url: '{% url "availability_edit" room.id %}',
    // Rest of the AJAX configuration
    // ...
  });
});
