create or alter view sm_jay_z as
with counts as (
select
	j.album_title,
	j.song,
	count(*) as 'rows'
from dbo.jay_z as j
group by
	j.album_title,
	j.song
)
select
	j.album_title,
	j.song,
	j.track,
	j.collaborator_name,
	case
		when j.collaborator_gender = 'Female' then 'F'
		when j.collaborator_gender = 'Male' then 'M'
		else 'Unknown'
	end as 'collaborator_gender_short',
	j.collaborator_gender,
	j.collaborator_birth_year,
	j.collaborator_city,
	j.collaborator_state,
	j.producers,
	s.year as 'streams_year',
	s.streams as 'streams',
	round(s.streams * s.revenue_per_stream, 2) as 'revenue',
	round(s.streams / cts.rows, 0) as 'streams_norm',
	round((s.streams * s.revenue_per_stream) / cts.rows, 2) as 'revenue_norm',
	c.*,
	getdate() as 'last_update'
from dbo.jay_z as j
left join dbo.jay_z_streams as s on s.song = j.song
left join counts as cts on cts.song = j.song
left join dbo.calendar_jay_z as c on c.datetime = j.date