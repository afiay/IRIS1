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