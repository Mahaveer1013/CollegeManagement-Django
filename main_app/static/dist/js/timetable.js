document.addEventListener('DOMContentLoaded', function() {
    const departmentField = document.getElementById('id_department');
    const classField = document.getElementById('id_class_name');

    departmentField.addEventListener('change', function() {
        const departmentId = this.value;

        fetch(`/admin/get_classes_by_department/?department_id=${departmentId}`)
            .then(response => response.json())
            .then(data => {
                classField.innerHTML = '';
                data.forEach(cls => {
                    const option = document.createElement('option');
                    option.value = cls.id;
                    option.text = `${cls.semester} sem - Section ${cls.section}`;
                    classField.appendChild(option);
                });
            });
    });
});
