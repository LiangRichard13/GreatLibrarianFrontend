import service from "@/utils/request";

export function getExperimentByProjectId(id) {
    return service({
        url: '/testProject',
        method: 'get',
        params: {
            pid: id
        }
    })
}

export function deleteById(data) {
    return service({
        url: '/testProject',
        method: 'delete',
        data:data
    })
}

export function addExpirement(data) {
    return service({
        url: '/testProject',
        method: 'post',
        data: data,
        headers: {
            'Content-Type': 'multipart/form-data'
          },
    })
}

export function editExpirement(data) {
    return service({
        url: '/testProject',
        method: 'put',
        data: data
    })
}

export function deleteOperationFile(data) {
    return service({
        url: '/testProjectConfig',
        method: 'delete',
        data: data
    })
}

export function checkOperationFile(data) {
    return service({
        url: '/testProjectConfig',
        method: 'post',
        data: data
    })
}

export function generateOperationFile(id) {
    return service({
        url: '/testProjectConfig',
        method: 'get',
        params: {tPid:id}
    })
}

// export function updateOperationFile(data) {
//     return service({
//         url: '/testProjectConfig',
//         method: 'put',
//         params: {choose:2},
//         data:data
//     })
// }