CREATE OR REPLACE FUNCTION public.get_full_info_about_top_largest_file(
	rlimit integer,
	roffset integer DEFAULT 0::int,
	dir_name character varying DEFAULT NULL::character varying
)
    RETURNS setof public.files as
$$
BEGIN
    IF (dir_name is not null) then
      RETURN QUERY SELECT
	  					fb.id,
						fb.file_id,
						fb.catalog_id,
						fb.file_name,
						fb.content_type,
						fb.file_size,
						fb.created_at,
						fb.updated_at
				  FROM public.files as fb
		  INNER JOIN public.catalogs as ctg ON fb.catalog_id = ctg.id
	   WHERE ctg.catalog_name=dir_name;
	else
    	RETURN QUERY SELECT * FROM public.files ORDER BY file_size DESC LIMIT rlimit OFFSET roffset;
   	end if;
END;
$$
LANGUAGE plpgsql VOLATILE;