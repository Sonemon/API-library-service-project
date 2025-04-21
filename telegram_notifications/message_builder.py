def build_borrowing_created_message(borrowing):
    return (
        f"📚 *New Borrowing Created*\n\n"
        f"*ID:* {borrowing.id}\n"
        f"*User:* {borrowing.user.email}\n"
        f"*Book:* {borrowing.book.title}\n"
        f"*Borrow Date:* {borrowing.borrow_date}\n"
        f"*Expected Return:* {borrowing.expected_return_date}"
    )

def build_borrowing_closed_message(borrowing):
    return (
        f"✅ Borrowing Closed\n"
        f"ID: {borrowing.id}\n"
        f"User: {borrowing.user.email}\n"
        f"Book: {borrowing.book.title}\n"
        f"Returned on: {borrowing.actual_return_date}"
    )
