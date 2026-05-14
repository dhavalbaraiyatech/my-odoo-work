if (navigator.userAgent.toLowerCase().indexOf('firefox') > -1 || navigator.userAgent.toLowerCase().indexOf('safari') > 88) {
    $('body').addClass('is-firefox');
}

$(document).ready(function () {
    var $contentH = $('.scroll-content-h');
    var $thumbH = $('.scrollbar-thumb-h');
    var $trackH = $('.scrollbar-track-h');

    function updateThumb() {
        var scrollLeft = $contentH.scrollLeft();
        var scrollWidth = $contentH[0].scrollWidth;
        var clientWidth = $contentH[0].clientWidth;
        var trackWidth = $trackH.width();

        var ratio = scrollLeft / (scrollWidth - clientWidth);
        var thumbWidth = (clientWidth / scrollWidth) * trackWidth;

        $thumbH.css({
            width: thumbWidth + 'px',
            left: (ratio * (trackWidth - thumbWidth)) + 'px'
        });
    }

    $contentH.on('scroll', updateThumb);
    updateThumb();

    var isDragging = false;
    var startX, startLeft;

    $thumbH.on('mousedown', function (e) {
        isDragging = true;
        startX = e.clientX;
        startLeft = parseInt($thumbH.css('left'), 10) || 0;
        $('body').css('user-select', 'none');
    });

    $(document).on('mousemove', function (e) {
        if (!isDragging) return;
        var dx = e.clientX - startX;
        var trackWidth = $trackH.width();
        var thumbWidth = $thumbH.width();
        var newLeft = startLeft + dx;

        newLeft = Math.max(0, Math.min(trackWidth - thumbWidth, newLeft));
        $thumbH.css('left', newLeft + 'px');

        var ratio = newLeft / (trackWidth - thumbWidth);
        $contentH.scrollLeft(ratio * ($contentH[0].scrollWidth - $contentH[0].clientWidth));
    });

    $(document).on('mouseup', function () {
        isDragging = false;
        $('body').css('user-select', '');
    });
});