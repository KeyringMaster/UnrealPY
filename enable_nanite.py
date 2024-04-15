import unreal



actors = unreal.EditorActorSubsystem().get_selected_level_actors()

def enableNanite(staticMeshActor):
    """
    Enable Nanite on static mesh associated with static mesh actor.
    """
    staticMesh = staticMeshActor.static_mesh_component.static_mesh
    if staticMesh:
        # get mesh nanite settings
        meshNaniteSettings = staticMesh.get_editor_property('nanite_settings')
        if not meshNaniteSettings.enabled:
            meshNaniteSettings.enabled = True
            # classes that inherit from EditorSubsystem need to be instatiated
            unreal.StaticMeshEditorSubsystem().set_nanite_settings(staticMesh,meshNaniteSettings, apply_changes=True)


for actor in actors:

    scene = actor.root_component

    child = scene.get_children_components(True)
    typed_child = [c for c in child if isinstance(c, unreal.StaticMeshComponent)]

    for each in typed_child:
        oname = str(each.get_fname())
        staticMesh = each.static_mesh

        if staticMesh:
            meshNaniteSettings = staticMesh.get_editor_property('nanite_settings')
            if not meshNaniteSettings.enabled:
                meshNaniteSettings.enabled = True
                unreal.StaticMeshEditorSubsystem().set_nanite_settings(staticMesh,meshNaniteSettings, apply_changes=True)



