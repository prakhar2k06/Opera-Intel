from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from ..database.repositories import exceptions as repo_exc
from ..domain.assets import exceptions as asset_exc
from ..domain.graph import exceptions as graph_exc
from ..domain.relationships import exceptions as relationship_exc
from ..domain.rules import exceptions as rule_exc


def register_exception_handlers(app: FastAPI) -> None:
    register_repo_exception_handlers(app)
    register_asset_exception_handlers(app)
    register_graph_exception_handlers(app)
    register_relationship_exception_handlers(app)
    register_rule_exception_handlers(app)


def register_repo_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(repo_exc.AssetTypeNotFoundException)
    def asset_type_not_found_exception_handler(
        request: Request, exc: repo_exc.AssetTypeNotFoundException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": "asset_type_not_found",
                "message": "AssetType not found.",
            },
        )

    @app.exception_handler(repo_exc.AssetNotFoundException)
    def asset_not_found_exception_handler(
        request: Request, exc: repo_exc.AssetNotFoundException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"code": "asset_not_found", "message": "Asset not found."},
        )

    @app.exception_handler(repo_exc.RelationshipTypeNotFoundException)
    def relationship_type_not_found_exception_handler(
        request: Request, exc: repo_exc.RelationshipTypeNotFoundException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": "relationship_type_not_found",
                "message": "RelationshipType not found.",
            },
        )

    @app.exception_handler(repo_exc.RelationshipNotFoundException)
    def relationship_not_found_exception_handler(
        request: Request, exc: repo_exc.RelationshipNotFoundException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": "relationship_not_found",
                "message": "Relationship not found.",
            },
        )


def register_asset_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(asset_exc.DuplicatePropertyException)
    def duplicate_property_exception_handler(
        request: Request, exc: asset_exc.DuplicatePropertyException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "code": "duplicate_property",
                "message": "A property with this name already exists in the AssetType.",
            },
        )

    @app.exception_handler(asset_exc.DuplicateStateException)
    def duplicate_state_exception_handler(
        request: Request, exc: asset_exc.DuplicateStateException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "code": "duplicate_state",
                "message": "A state with this name already exists in the AssetType.",
            },
        )

    @app.exception_handler(asset_exc.DuplicateTransitionException)
    def duplicate_transition_exception_handler(
        request: Request, exc: asset_exc.DuplicateTransitionException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "code": "duplicate_transition",
                "message": "An transition with similar definition already exists on the AssetType.",
            },
        )

    @app.exception_handler(asset_exc.DuplicateRuleException)
    def duplicate_rule_exception_handler(
        request: Request, exc: asset_exc.DuplicateRuleException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "code": "duplicate_rule",
                "message": "An rule with similar definition already exists on the AssetType.",
            },
        )

    @app.exception_handler(asset_exc.UnpublishedAssetTypeException)
    def unpublished_asset_type_exception_handler(
        request: Request, exc: asset_exc.UnpublishedAssetTypeException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "code": "unpublished_asset_type",
                "message": "Cannot create an Asset from an unpublished AssetType.",
            },
        )

    @app.exception_handler(asset_exc.AssetTypeSchemaLockedException)
    def asset_type_schema_locked_exception_handler(
        request: Request, exc: asset_exc.AssetTypeSchemaLockedException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "code": "asset_type_schema_locked",
                "message": "Published AssetTypes cannot be mutated.",
            },
        )

    @app.exception_handler(asset_exc.InvalidAssetStateTransitionException)
    def invalid_asset_state_transition_exception_handler(
        request: Request, exc: asset_exc.InvalidAssetStateTransitionException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "code": "invalid_asset_state_transition",
                "message": "The requested state transition is not allowed.",
            },
        )

    @app.exception_handler(asset_exc.InitialStateNotSetException)
    def initial_state_not_set_exception_handler(
        request: Request, exc: asset_exc.InitialStateNotSetException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "code": "initial_state_not_set",
                "message": "A stateful AssetType must define an initial state before publishing.",
            },
        )

    @app.exception_handler(asset_exc.MissingPropertyException)
    def missing_property_exception_handler(
        request: Request, exc: asset_exc.MissingPropertyException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "code": "missing_property",
                "message": "A required property was not provided.",
            },
        )

    @app.exception_handler(asset_exc.UnknownPropertyException)
    def unknown_property_exception_handler(
        request: Request, exc: asset_exc.UnknownPropertyException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "code": "unknown_property",
                "message": "The referenced property is not defined in this AssetType.",
            },
        )

    @app.exception_handler(asset_exc.InvalidPropertyValueException)
    def invalid_property_value_exception_handler(
        request: Request, exc: asset_exc.InvalidPropertyValueException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "code": "invalid_property_value",
                "message": "The provided value is invalid for this property.",
            },
        )

    @app.exception_handler(asset_exc.InvalidTargetStateException)
    def invalid_target_state_exception_handler(
        request: Request, exc: asset_exc.InvalidTargetStateException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "code": "invalid_target_state",
                "message": "The target state is invalid or is not defined in this AssetType..",
            },
        )

    @app.exception_handler(asset_exc.StateNotInAssetTypeException)
    def state_not_in_asset_type_exception_handler(
        request: Request, exception: asset_exc.StateNotInAssetTypeException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "code": "state_not_in_asset_type",
                "message": "State does not exist in AssetType.",
            },
        )

    @app.exception_handler(asset_exc.InvalidStateDefinitionException)
    def invalid_state_definition_exception_handler(
        request: Request, exception: asset_exc.InvalidStateDefinitionException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "code": "invalid_state_definition",
                "message": "Invalid state definition provided.",
            },
        )

    @app.exception_handler(asset_exc.InvalidRuleDefinitionException)
    def invalid_rule_definition_exception_handler(
        request: Request, exception: asset_exc.InvalidRuleDefinitionException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "code": "invalid_rule_definition",
                "message": "Invalid rule definition provided.",
            },
        )

    @app.exception_handler(asset_exc.InvalidStateTransitionException)
    def invalid_state_transition_exception_handler(
        request: Request, exception: asset_exc.InvalidStateTransitionException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "code": "invalid_state_transition",
                "message": "Invalid state transition definition provided.",
            },
        )

    @app.exception_handler(asset_exc.PropertyNotInAssetTypeException)
    def property_not_in_asset_type_exception_handler(
        request: Request, exception: asset_exc.PropertyNotInAssetTypeException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "code": "property_not_in_asset_type",
                "message": "The referenced property is not defined in this AssetType.",
            },
        )


def register_graph_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(graph_exc.DuplicateRelationshipException)
    def duplicate_relationship_exception_handler(
        request: Request, exc: graph_exc.DuplicateRelationshipException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "code": "duplicate_relationship",
                "message": "This Relationship already exists in the OperationalGraph.",
            },
        )

    @app.exception_handler(graph_exc.DuplicateAssetException)
    def duplicate_asset_exception_handler(
        request: Request, exc: graph_exc.DuplicateAssetException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "code": "duplicate_asset",
                "message": "This Asset already exists in the OperationalGraph.",
            },
        )

    @app.exception_handler(graph_exc.InvalidGraphAssetException)
    def invalid_graph_asset_exception_handler(
        request: Request, exc: graph_exc.InvalidGraphAssetException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "code": "invalid_graph_asset",
                "message": "Invalid Asset definition provided.",
            },
        )

    @app.exception_handler(graph_exc.InvalidGraphRelationshipException)
    def invalid_graph_relationship_exception_handler(
        request: Request, exc: graph_exc.InvalidGraphRelationshipException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "code": "invalid_graph_relationship",
                "message": "Invalid Relationship definition provided.",
            },
        )

    @app.exception_handler(graph_exc.AssetNotInGraphException)
    def asset_not_in_graph_exception(
        request: Request, exc: graph_exc.AssetNotInGraphException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "code": "asset_not_in_graph",
                "message": "The referenced Asset is not present in the OperationalGraph.",
            },
        )


def register_relationship_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(relationship_exc.RelationshipTypeMismatchException)
    def relationship_type_mismatch_expection_handler(
        request: Request, exc: relationship_exc.RelationshipTypeMismatchException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "code": "relationship_type_mismatch",
                "message": "The source or target Asset does not match the corresponding AssetType required by the RelationshipType.",
            },
        )

    @app.exception_handler(relationship_exc.InvalidRelationshipTypeException)
    def invalid_relationship_type_expection_handler(
        request: Request, exc: relationship_exc.InvalidRelationshipTypeException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "code": "invalid_relationship_type",
                "message": "The provided RelationshipType is invalid.",
            },
        )

    @app.exception_handler(relationship_exc.InvalidRelationshipAssetException)
    def invalid_relationship_asset_expection_handler(
        request: Request, exc: relationship_exc.InvalidRelationshipAssetException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "code": "invalid_relationship_asset",
                "message": "The provided Asset is invalid for this Relationship.",
            },
        )

    @app.exception_handler(relationship_exc.SelfRelationshipException)
    def self_relationship_expection_handler(
        request: Request, exc: relationship_exc.InvalidRelationshipAssetException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "code": "self_relationship",
                "message": "The source and target cannot be the same.",
            },
        )


def register_rule_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(rule_exc.InvalidTriggerDefinitionException)
    def invalid_trigger_definition_exception_handler(
        request: Request, exc: rule_exc.InvalidTriggerDefinitionException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "code": "invalid_trigger_definition",
                "message": "Invalid trigger definition provided.",
            },
        )

    @app.exception_handler(rule_exc.InvalidRuleDefinitionException)
    def invalid_rule_definition_exception_handler(
        request: Request, exc: rule_exc.InvalidRuleDefinitionException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "code": "invalid_rule_definition",
                "message": "Invalid rule definition provided.",
            },
        )

    @app.exception_handler(rule_exc.InvalidConditionDefinitionException)
    def invalid_condition_definition_exception_handler(
        request: Request, exc: rule_exc.InvalidConditionDefinitionException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "code": "invalid_condition_definition",
                "message": "Invalid condition definition provided.",
            },
        )

    @app.exception_handler(rule_exc.InvalidActionDefinitionException)
    def invalid_action_definition_exception_handler(
        request: Request, exc: rule_exc.InvalidActionDefinitionException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "code": "invalid_action_definition",
                "message": "Invalid action definition provided.",
            },
        )
