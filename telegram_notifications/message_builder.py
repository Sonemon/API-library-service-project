def build_borrowing_created_message(borrowing):
    return (
        f"📚 *New Borrowing Created*\n\n"
        f"*ID:* {borrowing.id}\n"
        f"*User:* {borrowing.user.email}\n"
        f"*Book:* {borrowing.book.title}\n"
        f"*Borrow Date:* {borrowing.borrow_date}\n"
        f"*Expected Return:* {borrowing.expected_return_date}"
    )

def build_borrowing_updated_message(before, after):
    changes = []
    for field in ["borrow_date", "expected_return_date", "actual_return_date"]:
        old = getattr(before, field)
        new = getattr(after, field)
        if old != new:
            changes.append(f"*{field.replace('_', ' ').title()}*: {old} → {new}")
    changes_text = "\n".join(changes) or "No visible changes."

    return (
        f"🔄 *Borrowing Updated*\n\n"
        f"*ID:* {before.id}\n"
        f"{changes_text}"
    )

def build_borrowing_closed_message(borrowing):
    return (
        f"✅ *Borrowing Closed*\n\n"
        f"*ID:* {borrowing.id}\n"
        f"*Book:* {borrowing.book.title}\n"
        f"*Returned At:* {borrowing.actual_return_date}"
    )
