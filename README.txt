CAKE TOWN - Stage 7
====================
Features:
- Customer QR/table URL support: /?table=05
- Customer name + 10-digit phone
- Menu, cart, total, order placement
- Customer order tracking
- Admin login: Cake Town / mohan
- Admin new-order count
- Automatic admin refresh every 2.5 seconds
- Sound alert for newly detected NEW orders
- Browser notification permission
- Order status: NEW, ACCEPTED, PREPARING, READY, DELIVERED, CANCELLED

Run:
1. pip install -r requirements.txt
2. python app.py
3. Customer: http://localhost:5000/?table=05
4. Admin: http://localhost:5000/admin

Important:
This Stage 7 uses browser polling for a simple prototype. For reliable background notifications when the admin browser is closed, production should use HTTPS + Web Push/FCM or another push notification service.
