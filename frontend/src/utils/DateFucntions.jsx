export const calculateAge = (birthdateValue) => {
    const today = new Date();
    const birthDate = new Date(birthdateValue);
    
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();

    // Если текущий месяц меньше месяца рождения 
    // ИЛИ месяцы равны, но текущий день меньше дня рождения — возраст еще не наступил
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
    return age;
};