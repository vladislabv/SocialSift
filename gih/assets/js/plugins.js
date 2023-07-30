// place any jQuery/helper plugins in here, instead of separate, slower script files.
// $jQuery(function() {

//     var startIndex = localStorage.getItem("currentIndex");
//     if(startIndex == null)
//         startIndex = 0;

//     $('.slidecontainer').slidecontainer({
//     startSlide: startIndex,
//         mode: 'horizontal',
//         infiniteLoop: true,
//         auto: true,
//         autoStart: true,
//         autoDirection: 'next',
//         autoHover: true,
//         pause: 3000,
//         autoControls: false,
//         pager: true,
//         pagerType: 'full',
//         controls: true,
//         captions: true,
//         speed: 500,
//         onSlideAfter: function($slideElm, oldIndex, newIndex) {save($slideElm, oldIndex, newIndex)}
// });

//     function save($slideElm, oldIndex, newIndex) {
//         console.log(oldIndex + " " + newIndex);

//         localStorage.setItem("currentIndex", newIndex);
//     }
// })