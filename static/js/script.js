// document.getElementById('productfield').focus();
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