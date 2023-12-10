API_LIST = [
    {
        "name": "works_list",
        "description": "Returns a list of work items matching the request.",
        "arguments": [
            {
                "argument_name": "applies_to_part",
                "argument_description": "Filters for work belonging to any of the provided parts",
                "argument_type": "array of strings"
            },
            {
                "argument_name": "created_by",
                "argument_description": "Filters for work created by any of these users",
                "argument_type": "array of strings"
            },
            {
                "argument_name": "issue.priority",
                "argument_description": "Filters for issues with any of the provided priorities. Allowed values: p0, p1, p2, p3",
                "argument_type": "array of strings"
            },
            {
                "argument_name": "issue.rev_orgs",
                "argument_description": "Filters for issues with any of the provided Rev organizations",
                "argument_type": "array of strings"
            },
            {
                "argument_name": "limit",
                "argument_description": "The maximum number of works to return. The default is '50'",
                "argument_type": "integer (int32)"
            },
            {
                "argument_name": "owned_by",
                "argument_description": "Filters for work owned by any of these users",
                "argument_type": "array of strings"
            },
            {
                "argument_name": "stage.name",
                "argument_description": "Filters for records in the provided stage(s) by name",
                "argument_type": "array of strings"
            },
            {
                "argument_name": "ticket.needs_response",
                "argument_description": "Filters for tickets that need a response",
                "argument_type": "boolean"
            },
            {
                "argument_name": "ticket.rev_org",
                "argument_description": "Filters for tickets associated with any of the provided Rev organizations",
                "argument_type": "array of strings"
            },
            {
                "argument_name": "ticket.severity",
                "argument_description": "Filters for tickets with any of the provided severities. Allowed values: blocker, high, low, medium",
                "argument_type": "array of strings"
            },
            {
                "argument_name": "ticket.source_channel",
                "argument_description": "Filters for tickets with any of the provided source channels",
                "argument_type": "array of strings"
            },
            {
                "argument_name": "type",
                "argument_description": "Filters for work of the provided types. Allowed values: issue, ticket, task",
                "argument_type": "array of strings"
            },
            {
                "argument_name": "date_of_creation",
                "argument_description": "Filters for the date of creation of the work item. Allowed format: yyyy-MM-dd HH:mm:ss"
            },
            {
                "argument_name": "last_modified",
                "argument_description": "Filters for work items last modified since a specified date. Allowed format: yyyy-MM-dd HH:mm:ss"
            },
            {
                "argument_name": "target_close_date",
                "argument_description": "Filter for the timestamp for when the work is expected to be complete. Allowed format: yyyy-MM-dd HH:mm:ss"
            }
        ]
    },
    {
        "name": "summarize_objects",
        "description": "Summarizes a list of objects. The logic of how to summarize a particular object type is an internal implementation detail.",
        "arguments": [
            {
                "argument_name": "objects",
                "argument_description": "List of objects to summarize",
                "argument_type": "array of objects"
            }
        ]
    },

    {
        "name": "prioritize_objects",
        "description": "Returns a list of objects sorted by priority. The logic of what constitutes priority for a given object is an internal implementation detail.",
        "arguments": [
            {
                "argument_name": "objects",
                "argument_description": "A list of objects to be prioritized",
                "argument_type": "array of objects"
            }
        ]
    },
    {
        "name": "add_work_items_to_sprint",
        "description": "Adds the given work items to the sprint",
        "arguments": [
            {
                "argument_name": "work_ids",
                "argument_description": "A list of work item IDs to be added to the sprint.",
                "argument_type": "array of strings"
            },
            {
                "argument_name": "sprint_id",
                "argument_description": "The ID of the sprint to which the work items should be added",
                "argument_type": "string"
            }
        ]
    },
    {
        "name": "get_sprint_id",
        "description": "Returns the ID of the current sprint",
        "arguments": []
    },
    {
        "name": "get_similar_work_items",
        "description": "Returns a list of work items that are similar to the given work item",
        "arguments": [
            {
                "argument_name": "work_id",
                "argument_description": "The ID of the work item for which you want to find similar items",
                "argument_type": "string"
            }
        ]
    },
    {
        "name": "search_object_by_name",
        "description": "Given a search string, returns the id of a matching object in the system of record. If multiple matches are found, it returns the one where the confidence is highest.",
        "arguments": [
            {
                "argument_name": "query",
                "argument_description": "The search string, could be for example customer's name, part name, username.",
                "argument_type": "string"
            }
        ]
    },
    {
        "name": "create_actionable_tasks_from_text",
        "description": "Given a text, extracts actionable insights, and creates tasks for them, which are kind of a work item.",
        "arguments": [
            {
                "argument_name": "text",
                "argument_description": "The text from which the actionable insights need to be created.",
                "argument_type": "string"
            }
        ]
    },
    {
        "name": "who_am_i",
        "description": "Returns the ID of the current user",
        "arguments": []
    },
    {
        "name": "is_empty",
        "description": "Checks if a given list is empty and returns one of two lists based on the result.",
        "arguments": [
            {
                "argument_name": "list_to_check",
                "argument_description": "The list to be checked for emptiness.",
                "argument_type": "array"
            },
            {
                "argument_name": "options",
                "argument_description": "Two lists of objects. Returns the first one if the list_to_check is empty, otherwise returns the second one.",
                "argument_type": "array of arrays"
            }
        ]
    },
    {
        "name": "count",
        "description": "Returns the number of work items in the output of an API call.",
        "arguments": [
            {
                "argument_name": "objects",
                "argument_description": "A list of objects to be counted.",
                "argument_type": "array of objects"
            }
        ]
    },
    {
        "name": "works-create",
        "description": "Creates work items based on the provided parameters.",
        "arguments": [
            {
                "argument_name": "applies_to_part",
                "argument_description": "The part that the work applies to. Specifying a part is required when creating tickets and issues. Note: REQUIRED",
                "argument_type": "array of strings"
            },
            {
                "argument_name": "created_by",
                "argument_description": "The users that reported the work",
                "argument_type": "array of strings"
            },
            {
                "argument_name": "issue.priority",
                "argument_description": "The Priority of the work based upon impact and criticality. Allowed values: p0, p1, p2, p3",
                "argument_type": "string"
            },
            {
                "argument_name": "developed_with",
                "argument_description": "The IDs of the parts associated with work item",
                "argument_type": "array of strings"
            },
            {
                "argument_name": "owned_by",
                "argument_description": "The users that own the work. Note: REQUIRED",
                "argument_type": "array of strings"
            },
            {
                "argument_name": "stage.name",
                "argument_description": "Sets an objects initial stage",
                "argument_type": "string"
            },
            {
                "argument_name": "sprint",
                "argument_description": "The sprint that the issue belongs to",
                "argument_type": "string"
            },
            {
                "argument_name": "type",
                "argument_description": "Type of the work item. Allowed values: issue, ticket, task. Note: REQUIRED",
                "argument_type": "string"
            },
            {
                "argument_name": "target_close_date",
                "argument_description": "Timestamp for when the work is expected to be complete. Allowed format: yyyy-MM-dd HH:mm:ss",
                "argument_type": "date"
            },
            {
                "argument_name": "title",
                "argument_description": "Title of the work object; Note: REQUIRED. Allowed values: issue, ticket",
                "argument_type": "string"
            }
        ]
    },
    {
        "name": "works-delete",
        "description": "Deletes a work item.",
        "arguments": [
            {
                "argument_name": "id",
                "argument_description": "The work's ID",
                "argument_type": "array of objects"
            }
        ]
    },
    {
        "name": "works-update",
        "description": "Updates a work item's information",
        "arguments": [
            {
                "argument_name": "id",
                "argument_description": "id of the work item to be updated. REQUIRED.",
                "argument_type": "array of strings"
            },
            {
                "argument_name": "applies_to_part",
                "argument_description": "Updates the part(s) that the work item applies to.",
                "argument_type": "array of strings"
            },
            {
                "argument_name": "created_by",
                "argument_description": "Sets the users that reported the work to the provided user IDs",
                "argument_type": "array of strings"
            },
            {
                "argument_name": "owned_by",
                "argument_description": "Sets the owner IDs to the provided user IDs. This must not be empty",
                "argument_type": "array of strings"
            },
            {
                "argument_name": "stage.name",
                "argument_description": "The updated name of the stage, otherwise unchanged if not set",
                "argument_type": "string"
            },
            {
                "argument_name": "type",
                "argument_description": "Updates the type of the work item. Allowed values: issue, ticket, task",
                "argument_type": "string"
            },
            {
                "argument_name": "target_close_date",
                "argument_description": "Updates the timestamp for when the work is expected to complete",
                "argument_type": "date"
            },
            {
                "argument_name": "title",
                "argument_description": "Updated title of the work object, or unchanged if not provided",
                "argument_type": "string"
            },
            {
                "argument_name": "priority",
                "argument_description": "Updates the priority of the work item. Allowed values: p0, p1, p2, p3",
                "argument_type": "string"
            }
        ]
    },
    {
        "name": "rev-orgs-create",
        "description": "Creates a Rev organization based on provided parameters.",
        "arguments": [
            {
                "argument_name": "description",
                "argument_description": "Description of the Rev organization",
                "argument_type": "string "
            },
            {
                "argument_name": "display_name",
                "argument_description": "Name of the Rev organization",
                "argument_type": "string"
            },
            {
                "argument_name": "environment",
                "argument_description": "The environment of the Org. Defaults to 'production' if not specified.",
                "argument_type": "string"
            }
        ]
    },
    {
        "name": "rev-orgs-delete",
        "description": "Deletes a Rev organization.",
        "arguments": [
            {
                "argument_name": "id",
                "argument_description": "Id of the Rev organization to be deleted",
                "argument_type": "string "
            }
        ]
    },

    {
        "name": "rev-orgs-update",
        "description": "Creates a Rev organization based on provided parameters.",
        "arguments": [
            {
                "argument_name": "description",
                "argument_description": "Description of the Rev organization",
                "argument_type": "string "
            },
            {
                "argument_name": "display_name",
                "argument_description": "Name of the Rev organization",
                "argument_type": "string"
            },
            {
                "argument_name": "environment",
                "argument_description": "The environment of the Org. Defaults to 'production' if not specified.",
                "argument_type": "string"
            },
            {
                "argument_name": "id",
                "argument_description": "The ID of Rev organization to update.",
                "argument_type": "string"
            }
        ]
    },
    {
        "name": "get_works_id",
        "description": "Get's the work id of the input objects",
        "arguments": [
            {
                "argument_name": "objects",
                "argument_description": "List of objects to get ID of",
                "argument_type": "array of objects"
            }
        ]
    },
    {
        "name": "get_current_date",
        "description": "Get's the current date",
        "arguments": []
    }

]