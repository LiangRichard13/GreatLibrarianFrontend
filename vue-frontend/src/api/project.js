import service from "@/utils/request";

export function addProject(data) {
    return service({
        url: '/project',
        method: 'post',
        data: data
    })
}

export function getProjectsByUseId(id) {
    return service({
        url: '/project',
        method: 'get',
        params: {
            uid: id
        }
    })
}

export function deleteById(id) {
    return service({
        url: '/project',
        method: 'delete',
        params: {
            id: id
        }
    })
}

export function addFriendsToProject(data) {
    return service({
        url: '/projectCollaborate',
        method: 'post',
        data: data
    })
}

export function getCollaborateProjectsByUserId(id) {
    return service({
        url: '/project/projectCollaborate/getCollaborateProjectsByUserId',
        method: 'get',
        params: {
            id: id
        }
    })
}

export function getCollaboratorsByProjectId(id) {
    return service({
        url: '/project/projectCollaborate/getCollaboratorsByProjectId',
        method: 'get',
        params: {
            id: id
        }
    })
}

export function getProjectByExpirementId(id) {
    return service({
        url: '/project/getProjectByExpirementId',
        method: 'get',
        params: {
            id: id
        }
    })
}