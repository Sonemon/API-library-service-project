def build_borrowing_created_message(borrowing):
    return (
        f"📚 *New Borrowing Created*\n"
        f"ID: {borrowing.id}\n"
        f"User: {borrowing.user.email} (id: {borrowing.user.id})\n"
        f"Book: {borrowing.book.title} (id: {borrowing.book.id})\n"
        f"Borrow Date: {borrowing.borrow_date.strftime("%Y-%m-%d %H:%M")}\n"
        f"Expected Return: {borrowing.expected_return_date}"
    )

def build_borrowing_closed_message(borrowing):
    return (
        f"✅ Borrowing Closed\n"
        f"ID: {borrowing.id}\n"
        f"User: {borrowing.user.email} (id: {borrowing.user.id})\n"
        f"Book: {borrowing.book.title} (id: {borrowing.book.id})\n"
        f"Returned on: {borrowing.actual_return_date.strftime("%Y-%m-%d %H:%M")}"
    )
