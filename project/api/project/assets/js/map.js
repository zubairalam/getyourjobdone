var map;
$(document).ready(function () {
    map = new GMaps({
        div: '#map',
        lat: 51.524079,
        lng: -0.102652,
    });
    map.addMarker({
        lat: 51.524079,
        lng: -0.102652,
        title: 'Address',
        infoWindow: {
            content: '<h5 class="title">XeonTek Ltd</h5><p><span class="region">145-157 St John Street, London</span><br><span class="postal-code">EC1V 4PW</span><br><span class="country-name">UK</span></p>'
        }

    });
});