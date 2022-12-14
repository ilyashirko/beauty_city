$(document).ready(function() {
	$('.salonsSlider').slick({
		arrows: true,
	  slidesToShow: 4,
	  infinite: true,
	  prevArrow: $('.salons .leftArrow'),
	  nextArrow: $('.salons .rightArrow'),
	  responsive: [
	    {
	      breakpoint: 991,
	      settings: {
	        
	      	centerMode: true,
  			//centerPadding: '60px',
	        slidesToShow: 2
	      }
	    },
	    {
	      breakpoint: 575,
	      settings: {
	        slidesToShow: 1
	      }
	    }
	  ]
	});
	$('.servicesSlider').slick({
		arrows: true,
	  slidesToShow: 4,
	  prevArrow: $('.services .leftArrow'),
	  nextArrow: $('.services .rightArrow'),
	  responsive: [
	  	{
	      breakpoint: 1199,
	      settings: {
	        

	        slidesToShow: 3
	      }
	    },
	    {
	      breakpoint: 991,
	      settings: {
	        
	      	centerMode: true,
  			//centerPadding: '60px',
	        slidesToShow: 2
	      }
	    },
	    {
	      breakpoint: 575,
	      settings: {
	        slidesToShow: 1
	      }
	    }
	  ]
	});

	$('.mastersSlider').slick({
		arrows: true,
	  slidesToShow: 4,
	  prevArrow: $('.masters .leftArrow'),
	  nextArrow: $('.masters .rightArrow'),
	  responsive: [
	  	{
	      breakpoint: 1199,
	      settings: {
	        

	        slidesToShow: 3
	      }
	    },
	    {
	      breakpoint: 991,
	      settings: {
	        

	        slidesToShow: 2
	      }
	    },
	    {
	      breakpoint: 575,
	      settings: {
	        slidesToShow: 1
	      }
	    }
	  ]
	});

	$('.reviewsSlider').slick({
		arrows: true,
	  slidesToShow: 4,
	  prevArrow: $('.reviews .leftArrow'),
	  nextArrow: $('.reviews .rightArrow'),
	  responsive: [
	  	{
	      breakpoint: 1199,
	      settings: {
	        

	        slidesToShow: 3
	      }
	    },
	    {
	      breakpoint: 991,
	      settings: {
	        

	        slidesToShow: 2
	      }
	    },
	    {
	      breakpoint: 575,
	      settings: {
	        slidesToShow: 1
	      }
	    }
	  ]
	});

	// menu
	$('.header__mobMenu').click(function() {
		$('#mobMenu').show()
	})
	$('.mobMenuClose').click(function() {
		$('#mobMenu').hide()
	})

	new AirDatepicker('#datepickerHere')

	var acc = document.getElementsByClassName("accordion");
	var i;

	for (i = 0; i < acc.length; i++) {
		console.log('accordeon click')
	  acc[i].addEventListener("click", function(e) {
	  	e.preventDefault()
	    this.classList.toggle("active");
	    var panel = $(this).next()
	    panel.hasClass('active') ?  
	    	 panel.removeClass('active')
	    	: 
	    	 panel.addClass('active')
	  });
	}


	$(document).on('click', '.accordion__block', function(e) {
		let thisName,thisAddress;
		console.log('accordion__block click')
		thisName = $(this).find('> .accordion__block_intro').text()
		thisAddress = $(this).find('> .accordion__block_address').text()
		var jsonData = JSON.parse(document.querySelector('#jsonData').getAttribute('data-json'));
		var salons = JSON.parse(document.querySelector('#json_salons').getAttribute('data-json'));
		var specializations = JSON.parse(document.querySelector('#specializations').getAttribute('data-json'));
		var salons_titles = Object.keys(salons)
		console.log(specializations)
		for (i in salons_titles) {
			if (thisName === salons_titles[i]) {
				var html = `<div class="accordion__block fic">
								<div class="accordion__block_elems fic">
									<img src="img/masters/avatar/all.svg" alt="avatar" class="accordion__block_img">
									<div class="accordion__block_master">?????????? ????????????</div>
								</div>
							</div>`;
				for (var person in jsonData) {
					var temp = `<div class="accordion__block fic">
									<div class="accordion__block_elems fic">
										<img style="width: 30px" src="` + jsonData[person]['image'] + `" alt="avatar" class="accordion__block_img">
										<div class="accordion__block_master">` + jsonData[person]['name'] + `</div>
									</div>
									<div class="accordion__block_prof">` + jsonData[person]['specialization'] + `</div>
								</div>`
					html += temp
					
					
				}
				$('.service__masters > .panel').html(html)
				

				var all_spec_html = ``
				for (var spec in specializations) {
					var current_spec = specializations[spec]['value']
					var html = `<div class="accordion__block_items">`
					var current_procesdures = salons[thisName]['procedures'][current_spec]
					for (var i in current_procesdures) {
						console.log(current_procesdures[i])
						var temp = `<div class="accordion__block_item fic">
										<div class="accordion__block_item_intro">` + current_procesdures[i]['title'] + `</div>
										<div class="accordion__block_item_address">` + current_procesdures[i]['price'] + ` ???</div>
									</div>`
						html += temp
					html += `</div>`
					}
					$('.' + specializations[spec]['hash']).html(html)
					
				}
				$('.accordion__block_item').click(function(e) {
					let thisName,thisAddress;
					thisName = $(this).find('> .accordion__block_item_intro').text()
					thisAddress = $(this).find('> .accordion__block_item_address').text()
					$(this).parent().parent().parent().parent().find('> button.active').addClass('selected').text(thisName + '  ' +thisAddress)
					// $(this).parent().parent().parent().parent().find('> button.active').click()
					// $(this).parent().parent().parent().addClass('hide')
					setTimeout(() => {
						$(this).parent().parent().parent().parent().find('> button.active').click()
					}, 200)
				})

				
				// var specializations = salons[thisName]['procedures']
				// var all_spec_html = ``
				// for (var spec in specializations) {
				// 	var spec_html = `<button class="accordion">` + spec + `</button>
				// 						<div class="panel"><div class="accordion__block_items">
				// 						`
				// 	var procedures = salons[thisName]['procedures'][spec]
				// 	for (var procedure in procedures) {
				// 			var temp = `<div class="accordion__block_item fic">
				// 							<div class="accordion__block_item_intro">` + procedures[procedure]['title'] + `</div>
				// 							<div class="accordion__block_item_address">` + procedures[procedure]['price'] + ` ???</div>
				// 						</div>`
				// 			spec_html += temp
				// 	}										
				// 	spec_html += `</div></div>`
				// 	all_spec_html += spec_html
				// }
				// $('.service__specializations > .panel').html(all_spec_html)
			}
		}

		$(this).parent().parent().find('> button.active').addClass('selected').text(thisName + '  ' +thisAddress)
		setTimeout(() => {
			$(this).parent().parent().find('> button.active').click()
		}, 200)
		
		// $(this).parent().addClass('hide')

		// console.log($(this).parent().parent().find('.panel').hasClass('selected'))
		
		// $(this).parent().parent().find('.panel').addClass('selected')
	})


	

	$(document).on('click', '.service__masters .accordion__block', function(e) {
		let clone = $(this).clone()
		console.log(clone)
		$(this).parent().parent().find('> button.active').html(clone)
	})

	// $('.accordion__block_item').click(function(e) {
	// 	const thisName = $(this).find('.accordion__block_item_intro').text()
	// 	const thisAddress = $(this).find('.accordion__block_item_address').text()
	// 	console.log($(this).parent().parent().parent().parent())
	// 	$(this).parent().parent().parent().parent().find('button.active').addClass('selected').text(thisName + '  ' +thisAddress)
	// })



	// $('.accordion__block_item').click(function(e) {
	// 	const thisChildName = $(this).text()
	// 	console.log(thisChildName)
	// 	console.log($(this).parent().parent().parent())
	// 	$(this).parent().parent().parent().parent().parent().find('button.active').addClass('selected').text(thisChildName)

	// })
	// $('.accordion.selected').click(function() {
	// 	$(this).parent().find('.panel').hasClass('selected') ? 
	// 	 $(this).parent().find('.panel').removeClass('selected')
	// 		:
	// 	$(this).parent().find('.panel').addClass('selected')
	// })


	//popup
	$('.header__block_auth').click(function(e) {
		e.preventDefault()
		$('#authModal').arcticmodal();
		// $('#confirmModal').arcticmodal();

	})

	$('.rewiewPopupOpen').click(function(e) {
		e.preventDefault()
		$('#reviewModal').arcticmodal();
	})
	$('.payPopupOpen').click(function(e) {
		e.preventDefault()
		$('#paymentModal').arcticmodal();
	})
	$('.tipsPopupOpen').click(function(e) {
		e.preventDefault()
		$('#tipsModal').arcticmodal();
	})
	
	$('.authPopup__form').submit(function() {
		$('#confirmModal').arcticmodal();
		return false
	})

	//service
	$('.time__items .time__elems_elem .time__elems_btn').click(function(e) {
		e.preventDefault()
		$('.time__elems_btn').removeClass('active')
		$(this).addClass('active')
		// $(this).hasClass('active') ? $(this).removeClass('active') : $(this).addClass('active')
	})

	$(document).on('click', '.servicePage', function() {
		if($('.time__items .time__elems_elem .time__elems_btn').hasClass('active') && $('.service__form_block > button').hasClass('selected')) {
			$('.time__btns_next').addClass('active')
		}
	})
	


})