from .exceptions import (
    S3Exception, FileException, ResourceNotFound, PermissionDenied,
    ResourceAlreadyExists, MissingParametersException
)


class GenericS3Exception(S3Exception):
    def __init__(self):
        super().__init__(
            reason='s3_exception',
            message='Something went wrong'
        )


class UnknownS3Content(S3Exception):
    def __init__(self):
        super().__init__(
            reason='s3_unknown_content',
            message='Unknown content type'
        )


class DeleteS3Failure(S3Exception):
    def __init__(self):
        super().__init__(
            reason='s3_delete_faillure',
            message='File could not be deleted'
        )


class InvalidFileType(FileException):
    def __init__(self, extension):
        super().__init__(
            reason='invalid_file_type',
            message='Content type {} not allowed'.format(
                extension)
        )


class MissingFileExtension(FileException):
    def __init__(self):
        super().__init__(
            reason='missing_file_extension',
            message='Missing file extention in filename'
        )


class ContactReceiverNotFound(ResourceNotFound):
    def __init__(self, user_id):
        super().__init__(
            message="Receiver with id {} not found for user".format(user_id),
            reason="contact_receiver_user"
        )


class TicketNotFound(ResourceNotFound):
    def __init__(self, ticket_id):
        super().__init__(
            message="Ticket with id {} not found".format(ticket_id),
            reason="ticket_not_found",
        )


class TicketReceiverNotFound(ResourceNotFound):
    def __init__(self):
        super().__init__(
            message="Ticket create failed",
            reason="ticket_receiver_user",
            errors=[
                {
                    "reason": "Receiver not found for user"
                }
            ]
        )


class TicketReceiverContactNotFound(ResourceNotFound):
    def __init__(self):
        super().__init__(
            message="Ticket create failed",
            reason="ticket_receiver_user",
            errors=[
                {
                    "reason": "Contact not found for receiver"
                }
            ]
        )


class TicketPackingSlipNotFound(ResourceNotFound):
    def __init__(self):
        super().__init__(
            message="Ticket create failed",
            reason="ticket_receiver_user",
            errors=[
                {
                    "reason": "Packing slip not found for receiver"
                }
            ]
        )


class ComplaintSolutionTicketNotFound(ResourceNotFound):
    def __init__(self, ticket_id):
        super().__init__(
            errors=[
                {
                    "reason": "Ticket does not exist",
                    "message": "cannot find related ticket",
                    "field": ticket_id
                }
            ],
            message="Complaint solution create failed.",
            reason="related_not_found"
        )


class ComplaintSolutionComplaintNotFound(ResourceNotFound):
    def __init__(self, complaint_id):
        super().__init__(
            errors=[
                {
                    "reason": "complaint does not exists",
                    "message": "cannot find related complaint",
                    "field": complaint_id
                }
            ],
            message="Complaint solution create failed.",
            reason="related_not_found"
        )


class ComplaintSolutionRelatedNotFound(ResourceNotFound):
    def __init__(self, related_type, related_id):
        super().__init__(
            errors=[
                {
                    "reason": "{related_type} with id {related_id} does "
                              "not exist".format(related_type=related_type,
                                                 related_id=related_id),
                    "message": "cannot find related object",
                    "field": related_id
                }
            ],
            message="Complaint solution create failed.",
            reason="related_not_found"
        )


class ComplaintSolutionSolutionNotFound(ResourceNotFound):
    def __init__(self, solution_id):
        super().__init__(
            errors=[
                {
                    "reason": "solution id does not exist",
                    "message": "cannot find related solution",
                    "field": solution_id
                }
            ],
            message="Complaint solution create failed.",
            reason="related_not_found"
        )


class ComplaintSolutionNotFound(ResourceNotFound):
    def __init__(self):
        super().__init__(
            errors=[
                {
                    "reason": "id does not exist",
                    "message": "Cannot find complaint solution",
                    "field": "id"
                }
            ],
            message="Complaint solution create failed.",
            reason="related_not_found"
        )


class ComplaintSolutionCleanupTicketNotFound(ResourceNotFound):
    def __init__(self, ticket_id):
        super().__init__(
            errors=[
                {
                    "reason": "ticket id does not exist",
                    "message": "cannot clean up ticket",
                    "field": ticket_id
                }
            ],
            message="Complaint solution create failed.",
            reason="related_not_found"
        )


class UnlinkedFilesNotFound(ResourceNotFound):
    def __init__(self, missing_file_ids):
        super().__init__(
            reason='not_all_unlinked_files_found',
            message='No unlinked files found with the following '
                    'ids: {}'.format(', '.join(missing_file_ids)))


class BudgetTypeNotFound(ResourceNotFound):
    def __init__(self, budget_type_id):
        super().__init__(
            errors=[
                {
                    "reason": "Budget type does not exist",
                    "message": "cannot find budget type",
                    "field": budget_type_id
                }
            ],
            message="Budget create failed.",
            reason="budget_bad_type"
        )


class TicketPermissionDenied(PermissionDenied):
    def __init__(self):
        super().__init__(
            message='User has no receivers',
            reason='ticket_permission_denied'
        )


class ReceiverPermissionDenied(PermissionDenied):
    def __init__(self):
        super().__init__(
            message='User has no access to receiver',
            reason='user_receiver_permission'
        )


class FilePermissionDenied(PermissionDenied):
    def __init__(self):
        super().__init__(
            reason='no_file_permission',
            message='User has no permission to delete this file'
        )


class DuplicateBudget(ResourceAlreadyExists):
    def __init__(self):
        super().__init__(
            message="This budget already exists.",
            data={
                "constraint": "budget_type_id, receiver_id, start"
            },
            reason="budget_duplicate"
        )


class MultiplePackingLineComplaints(ResourceAlreadyExists):
    def __init__(self, complaint_solution):
        super().__init__(
            message="Complaint solution create failed",
            reason="related_complaint_exists",
            errors=[
                {
                    "message": "Packing line already has a complaint."
                }
            ],
            data={
                "complaint": complaint_solution
            }
        )


class BlockingComplaints(ResourceAlreadyExists):
    def __init__(self, complaint_solutions):
        super().__init__(
            message="Complaint solution create failed",
            reason="related_complaint_exists",
            errors=[
                {
                    "message": "Cannot create complaint when blocking "
                               "complaint solution exists."
                }
            ],
            data={
                "complaint_solutions": complaint_solutions
            }
        )


class DuplicateComplaint(ResourceAlreadyExists):
    def __init__(self, complaint):
        super().__init__(
            message="Complaint solution create failed",
            reason="related_complaint_exists",
            errors=[
                {
                    "message": "This complaint has already been filed."
                }
            ],
            data={
                "complaint": complaint
            }
        )


class InvalidComplaint(ResourceAlreadyExists):
    def __init__(self, line_complaints):
        super().__init__(
            message="Complaint solution create failed",
            reason="related_complaint_exists",
            errors=[
                {
                    "message": "Invalid combination of complaints."
                }
            ],
            data={
                "complaint_solutions": [
                    {
                        "id": complaint_solution.id,
                        "level": "packing_line"
                    }
                ] for complaint_solution in line_complaints
            }
        )


class DuplicateFile(ResourceAlreadyExists):
    def __init__(self):
        super().__init__(
            reason='file_already_exists',
            message='Database error'
        )


class BudgetDeleteParamsMissing(MissingParametersException):
    def __init__(self):
        super().__init__(
            message="Delete parameters not sufficient",
            reason="budget_delete_params"
        )


class ActorTypeNotFound(ResourceNotFound):
    def __init__(self):
        super().__init__(
            errors=[
                {
                    "reason": "actor remote id does not exist",
                    "message": "cannot get actor"
                }
            ],
            message="Actor get failed.",
            reason="actor_type_not_found"
        )


class ActorNotFound(ResourceNotFound):
    def __init__(self):
        super().__init__(
            errors=[
                {
                    "reason": "actor was not found",
                    "message": "cannot get actor"
                }
            ],
            message="Actor get failed.",
            reason="actor_not_found"
        )
