from repositories.search_repo import (
    get_email_context_by_account
)

from services.email_qa_service import (
    answer_question
)


class EmailQAAgent:

    def ask(
        self,
        question,
        gmail_account_id
    ):

        try:

            emails = (
                get_email_context_by_account(
                    gmail_account_id
                )
            )

            context = []

            for email in emails:

                context.append(
                    f"""
    Category:
    {email.get('category')}

    Priority:
    {email.get('priority')}

    Summary:
    {email.get('short_summary')}

    Details:
    {email.get('detailed_summary')}
    """
                )

            return answer_question(
                question,
                "\n".join(context)
            )

        except Exception as e:

            print(
                f"EmailQAAgent failed: {e}"
            )