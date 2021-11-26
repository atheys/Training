create or alter view sm_titanic as
select
	t.id,
	t.survived,
	case
		when t.survived = 1 then 'Yes'
		else 'No'
	end as 'surived_label',
	case
		when t.survived = 1 then 0
		else 1
	end as 'surived_label_order',
	t.name,
	case
		when t.gender = 'male' then 'M'
		else 'F'
	end as 'gender',
	case
		when t.gender = 'male' then 'Male'
		else 'Female'
	end as 'gender_label',
	case
		when t.gender = 'male' then 0
		else 1
	end as 'gender_label_order',
	p.birthdate,
	round(p.height, 2) as 'height',
	round(p.weight, 2) as 'weight',
	round(p.bmi, 2) as 'bmi',
	case
		when p.bmi >= 25 then 1
		else 0
	end as 'overweight',
	case
		when p.bmi >= 25 then 'Yes'
		else 'No'
	end as 'overweight_label',
	case
		when p.bmi >= 25 then 0
		else 1
	end as 'overweight_label_order',
	t.age,
	case
		when t.age < 10 then '<10'
		when 10 <= t.age and t.age < 20 then '10-20'
		when 20 <= t.age and t.age < 30 then '20-30'
		when 30 <= t.age and t.age < 40 then '30-40'
		when 40 <= t.age and t.age < 50 then '40-50'
		when 50 <= t.age and t.age < 60 then '50-60'
		when 60 <= t.age then '60+'
		else 'Unknown'
	end as 'age_category',
	case
		when t.age < 10 then 0
		when 10 <= t.age and t.age < 20 then 1
		when 20 <= t.age and t.age < 30 then 2
		when 30 <= t.age and t.age < 40 then 3
		when 40 <= t.age and t.age < 50 then 4
		when 50 <= t.age and t.age < 60 then 5
		when 60 <= t.age then 6
		else 7
	end as 'age_category_order',
	t.class,
	t.siblings,
	t.children,
	t.cabin,
	case
		when t.cabin like '%A%' then 'A'
		when t.cabin like '%B%' then 'B'
		when t.cabin like '%C%' then 'C'
		when t.cabin like '%D%' then 'D'
		when t.cabin like '%E%' then 'E'
		when t.cabin like '%F%' then 'F'
		else 'Other'
	end as 'cabin_type',
	t.fare,
	t.embarked as 'embarked_short',
	case
		when t.embarked = 'S' then 'Southampton'
		when t.embarked = 'Q' then 'Queenstown'
		when t.embarked = 'C' then 'Charbourg'
		else 'Unknown'
	end as 'embarked',
	case
		when t.embarked = 'S' then 0
		when t.embarked = 'Q' then 2
		when t.embarked = 'C' then 1
		else 3
	end as 'embarked_order',
	c.*,
	getdate() as 'last_update'
from dbo.titanic t
left join dbo.titanic_passengers p on p.id = t.id
left join dbo.calendar_titanic c on c.datetime = p.birthdate