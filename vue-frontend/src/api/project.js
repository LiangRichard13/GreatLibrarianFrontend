import service from "@/utils/request";

export function addProject(data) {
    return service({
        url: '/project/addProject',
        method: 'post',
        data: data
    })
}

export function getProjectsByUseId(id) {
    return service({
        url: '/project/getProjectsByUserId',
        method: 'get',
        params: {
            id: id
        }
    })
}

export function deleteById(id) {
    return service({
        url: '/project/deleteById',
        method: 'delete',
        params: {
            id: id
        }
    })
}

export function addFriendsToProject(data) {
    return service({
        url: '/project/addFriendsToProject',
        method: 'post',
        data: data
    })
}

export function getCollaborateProjectsByUserId(id) {
    return service({
        url: '/project/getCollaborateProjectsByUseId',
        method: 'get',
        params: {
            id: id
        }
    })
}

export function getCollaboratorsByProjectId(id) {
    return service({
        url: '/project/getCollaboratorsByProjectId',
        method: 'get',
        params: {
            id: id
        }
    })
}

export function getProjectByExpirementId(id) {
    return service({
        url: '/project/getCollaboratorsByProjectId',
        method: 'get',
        params: {
            id: id
        }
    })
}