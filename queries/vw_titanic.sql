create or alter view vw_titanic as
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
	t.age,
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
	end as 'embarked_order'
from dbo.titanic t
left join dbo.titanic_passengers p on p.id = t.id