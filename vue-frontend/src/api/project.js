import service from "@/utils/request";

export function addProject(data) {
    return service({
        url: '/project',
        method: 'post',
        data: data
    })
}

export function addApiKeyToProject(data)
{
    return service(
        {
            url:'/projectAK',
            method:'post',
            data:data
        }
    )
}

export function addDataSetToProject(data)
{
    return service(
        {
            url:'/projectDS',
            method:'post',
            data:data
        }
    )
}

export function getProjectsByUserId(id) {
    return service({
        url: '/project',
        method: 'get',
        params: {
            uid: id
        }
    })
}

export function deleteById(data) {
    return service({
        url: '/project',
        method: 'delete',
        data:data
    })
}


// export function getCollaborateProjectsByUserId(id) {
//     return service({
//         url: '/project/projectCollaborate/getCollaborateProjectsByUserId',
//         method: 'get',
//         params: {
//             id: id
//         }
//     })
// }

// export function getCollaboratorsByProjectId(id) {
//     return service({
//         url: '/project/projectCollaborate/getCollaboratorsByProjectId',
//         method: 'get',
//         params: {
//             id: id
//         }
//     })
// }

// export function getProjectByExpirementId(id) {
//     return service({
//         url: '/project/getProjectByExpirementId',
//         method: 'get',
//         params: {
//             id: id
//         }
//     })
// }