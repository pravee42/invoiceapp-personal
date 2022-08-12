document.getElementById('productfield').focus();
document.getElementById('costumer_name_field').focus();

// function nameFunction() {
// 	const dd = document.getElementById('selecttype011').value;
// 	// dd === 'Cash'
// 	// 	? (document.getElementById('sendinvoiceform').action =
// 	// 			document.getElementById('sendinvoiceform').action + '0' + '/')
// 	// 	: null;
// }

function calculateTotal() {
	let total1 = 0;
	const type = document.getElementById('discounttype_select').value;
	const discount = document.getElementById('discount_field').value;
	const totalammount = document.getElementById('totalvalueammount').value;
	type === 'percent'
		? (total1 =
				parseInt(totalammount) -
				(parseInt(totalammount) * parseInt(discount)) / 100)
		: (total1 = parseInt(totalammount) - parseInt(discount));
	
	document.getElementById('totalvalueammount').value = parseInt(total1);

	const disper = dicsount + '%'
	const disp = 'Rs.' + dicsount

	type === 'percent'
		? (document.getElementById('discount_field').value = disper.toString())
		: (document.getElementById('discount_field').value = disp.toString());
	
}
function setfields(name) {
	let text = name.split(' + ');
	document.getElementById('productfield').value = text[0];
	document.getElementById('pricefield').value = text[1];
	document.getElementById('gstfield').value = text[2];
	document.getElementById('qtyfield').focus();
}

function setcostumerfields(name) {
	let text = name.split(' + ');
	document.getElementById('costumer_name_field').value = text[0];
	document.getElementById('customer_gst_field').value = text[1];
	// alert(window.location[28: 34]);
	let ll = window.location.href
	const total = document.getElementById('totalvalueammount').value
	ll = ll.slice(36,41)
	document.getElementById('sendinvoiceform').action = '/save/' + ll + '/' + total+ '/' + text[2] + '/';
	document.getElementById('refrence_number_field').focus();
}


function totalammountff() {
	const qty = document.getElementById('qtyfield').value;
	const price = document.getElementById('pricefield').value;
	const gst = document.getElementById('gstfield').value;
	let gstammount = parseInt(price) + (parseInt(price) * parseInt(gst)) / 100;
	let totalammount = parseInt(gstammount) * parseInt(qty);
	document.getElementById('totalfield').value = totalammount;
}

// function show_menu_expenses() {
// 	document.getElementById('menu_expenses').style.display = 'block';
// }
// function x() {
// 	let e = window.event;
// 	let keycode = e.keyCode;
// 	if (keycode == 17) {
// 		document.getElementById('products_model').style.display = 'block';
// 	}
// };

function callSearchfunction() {
	const searchField = document.querySelector('#search_products_field').value;
	if (window.event.keyCode == 13) {
		document.getElementById('search_table_tbody').innerHTML = ""
		if (searchField.trim().length > 1) {
			fetch(`/api/products/${searchField}/`)
				.then((res) => res.json())
				.then((data) => {
					if (data.length > 0) {
						document.getElementById('app_table').style.display = 'none';
						document.getElementById('search_table').style.display = '';
						data.forEach((product) => {
							document.getElementById('search_table_tbody').innerHTML += `
						<tr>
							<td>${product.product_name}</td>
							<td>${product.product_price}.00</td>
							<td>
								<button
								class="btn btn-outline-primary"
								id="${product.product_name} + ${product.product_price} + ${product.gst}"
								onclick="setfields(id)"
								data-bs-dismiss="offcanvas"
								aria-label="Close"
							>
								<i class="bi bi-check-all"></i>
							</button>
							</td>
						</tr>
					`;
							console.log(product.product_name);
						});
					} else {
						document.getElementById('search_table').style.display = 'none';
						document.getElementById('app_table').style.display = 'block';
					}
				});
		} else {
			document.getElementById('app_table').style.display = 'block';
			document.getElementById('search_table').style.display = 'none';
		}
	}
}