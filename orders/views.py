from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from cart.models import CartItem

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('cart_detail')
    
    total = sum(item.subtotal for item in cart_items)
    
    if request.method == 'POST':
        import uuid
        tracking_id = f"GLX-{uuid.uuid4().hex[:10].upper()}"
        
        address_line = request.POST.get('address_line')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pin_code = request.POST.get('pin_code')
        payment_method = request.POST.get('payment_method')
        
        order = Order.objects.create(
            user=request.user,
            total_price=total,
            payment_method=payment_method,
            address_line=address_line,
            city=city,
            state=state,
            pin_code=pin_code,
            tracking_id=tracking_id,
            status='Pending'
        )
        
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.discounted_price
            )
            # Reduce stock
            if item.product.stock >= item.quantity:
                item.product.stock -= item.quantity
                item.product.save()
            
        cart_items.delete()
        return redirect('order_success', order_id=order.id)
        
    return render(request, 'orders/checkout.html', {
        'total': total, 
        'cart_items': cart_items, 
        'payment_methods': Order.PAYMENT_CHOICES
    })

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})
